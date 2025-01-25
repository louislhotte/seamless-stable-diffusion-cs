import torch
from datasets import load_dataset
from transformers import CLIPTokenizer
from diffusers import UNet2DConditionModel
from peft import LoraConfig, get_peft_model
from torch.utils.data import DataLoader
from torchvision import transforms

ds = load_dataset("logo-wizard/modern-logo-dataset")
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32") #On peut mettre d'autres modèles
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5]),
])

def preprocess(example):
    example["input_ids"] = tokenizer(example["text"], truncation=True, padding="max_length").input_ids
    example["pixel_values"] = torch.stack([transform(img) for img in example["image"]])
    return example

ds = ds.map(preprocess, batched=True)
dataloader = DataLoader(ds["train"], batch_size=1, shuffle=True)

model = UNet2DConditionModel.from_pretrained("CompVis/stable-diffusion-v1-3")
config = LoraConfig(
    r=4,
    lora_alpha=16,
    target_modules=["attn1", "attn2"], #potentiellement à changer en fonction des layers target qu'on veut fine-tuner
    lora_dropout=0.05,
    bias="none"
)
model = get_peft_model(model, config)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

model.train()
for epoch in range(10):
    for batch in dataloader:
        optimizer.zero_grad()
        outputs = model(batch["pixel_values"], encoder_hidden_states=batch["input_ids"])
        loss = outputs.loss
        loss.backward()
        optimizer.step()

model.save_pretrained("lora-modern-logo-small")
