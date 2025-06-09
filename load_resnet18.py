import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

def load_model(checkpoint_path, device, num_classes=3):
    # Load ResNet18 với trọng số ImageNet
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    in_features = model.fc.in_features

    # Khởi tạo lại FC đúng như lúc train
    model.fc = nn.Sequential(
        nn.Dropout(p=0.6),
        nn.Linear(in_features, 512),
        nn.LayerNorm(512),
        nn.ReLU(),
        nn.Dropout(p=0.6),
        nn.Linear(512, num_classes)
    )

    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device)
    if isinstance(checkpoint, dict) and 'model' in checkpoint:
        model.load_state_dict(checkpoint['model'])
    else:
        model.load_state_dict(checkpoint)

    model.to(device)
    model.eval()
    print(f"Loaded model from {checkpoint_path} on {device}")
    return model
