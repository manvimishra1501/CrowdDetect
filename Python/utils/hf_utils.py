# utils/hf_utils

from transformers import AutoModelForImageClassification, AutoFeatureExtractor
import torch
from PIL import Image
import cv2


MODEL = None
EXTRACTOR = None

def load_hf_model(model_name="google/vit-base-patch16-224-in21k"):
    global MODEL, EXTRACTOR
    MODEL = AutoModelForImageClassification.from_pretrained(model_name)
    EXTRACTOR = AutoFeatureExtractor.from_pretrained(model_name)

def hf_inference(frame, model_name="google/vit-base-patch16-224-in21k"):
    global MODEL, EXTRACTOR
    if MODEL is None or EXTRACTOR is None:
        load_hf_model(model_name)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = EXTRACTOR(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = MODEL(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    top_prob, top_class = torch.max(probs, dim=1)
    return {"class_idx": int(top_class), "prob": float(top_prob)}