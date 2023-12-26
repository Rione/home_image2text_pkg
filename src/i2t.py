import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

def i2t_ros(msg, cache_dir="cache"):
    """
    + image2text
    ```python
    from image2text import i2t

    for text in i2t():
        print(text)
    ```

    args:
        camera_id: camera id, default: 0
        cache_dir: cache directory, default: "cache"
    yield:
        text: text of image
    """
    pub = rospy.Publisher("image2text", String, queue_size=1)
    bridge = CvBridge()
    cap = bridge.imgmsg_to_cv2(msg, "bgr8")

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir=cache_dir)
    device = get_device()

    print("Using device: ", device.upper())
    if (device == "cuda"):
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large", torch_dtype=torch.float16, cache_dir=cache_dir).to("cuda")
    else:
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir=cache_dir)

    while True:
        ret, frame = cap.read()
        if not ret:
            pass
        if device == "cuda":
            processor=processor(frame, "a photography of", return_tensors="pt").to(device, torch.float16)
        else:
            inputs = processor(frame, "a photography of", return_tensors="pt")
        out = model.generate(**inputs)
        pub.Publish(processor.decode(out[0], skip_special_tokens=True))
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
