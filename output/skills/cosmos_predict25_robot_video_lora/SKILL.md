---
name: cosmos_predict25_robot_video_lora
description: |
  Fine-tune NVIDIA Cosmos Predict 2.5 with LoRA/DoRA for robot video generation using Hugging Face Diffusers and PEFT.
  Triggers: cosmos fine-tuning, robot video generation, cosmos predict lora, dora video training, nvidia cosmos robotics
---

# Fine-Tuning NVIDIA Cosmos Predict 2.5 with LoRA/DoRA for Robot Video Generation

Fine-tune the Cosmos Predict 2.5 world foundation model using LoRA or DoRA adapters to generate realistic robot manipulation videos from a single image and text prompt.

## When to use

- "Fine-tune Cosmos Predict 2.5 for robot video generation"
- "Train a LoRA adapter on robot manipulation videos with Cosmos"
- "Generate robot task videos from an image and text prompt using Cosmos"
- "Set up DoRA fine-tuning for NVIDIA Cosmos world model"
- "Evaluate fine-tuned Cosmos video generation quality"

## How to use

### 1. Install dependencies

```bash
pip install -U "diffusers[torch]" transformers accelerate peft wandb
```

Requirements: Python 3.10+, PyTorch 2.5+ with CUDA, minimum 1x 80GB GPU (8x H100 recommended).

### 2. Prepare the dataset

Download and preprocess the GR1-100 robot manipulation dataset (92 training videos) and the GR00T-Eval test set (50 prompt/image pairs):

```bash
bash download_and_preprocess_datasets.sh
```

Expected structure:
```
gr1_dataset/
├── train/
│   ├── metas/*.txt
│   ├── videos/*.mp4
│   └── metadata.csv
└── test/
    ├── *.txt
    └── *.png
```

Datasets: [nvidia/GR1-100](https://huggingface.co/datasets/nvidia/GR1-100) and [nvidia/PhysicalAI-Robotics-GR00T-Eval](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-Eval).

### 3. Configure the LoRA/DoRA adapter

The training script freezes the base DiT, VAE, and text encoder, then attaches a LoRA adapter to the DiT attention and feedforward layers:

```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=32,                # Rank: 32 recommended, 8 for memory-constrained
    lora_alpha=32,       # Set equal to rank for scale factor 1.0
    target_modules=['to_q', 'to_k', 'to_v', 'to_out.0', 'ff.net.0.proj', 'ff.net.2'],
    use_dora=False,      # Set True for DoRA variant
)
```

**Choosing rank and method:**
- **LoRA r=32** (default): Best instruction following and quality (~50M trainable params)
- **LoRA r=8**: Memory-constrained setups, smaller adapter files
- **DoRA r=32**: Use if training instability is observed; adds magnitude decomposition

### 4. Train

```bash
export MODEL_NAME="nvidia/Cosmos-Predict2.5-2B"
export DATA_DIR="gr1_dataset/train"
export OUT_DIR="output/cosmos_lora"

accelerate launch --mixed_precision="bf16" train_cosmos_predict25_lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --revision diffusers/base/post-trained \
  --train_data_dir=$DATA_DIR \
  --train_batch_size=1 \
  --num_train_epochs=500 \
  --checkpointing_epochs=100 \
  --seed=0 \
  --output_dir=$OUT_DIR \
  --report_to=wandb \
  --height 432 --width 768 \
  --allow_tf32 --gradient_checkpointing \
  --lora_rank 32 --lora_alpha 32
```

Add `--use_dora` for the DoRA variant.

**Training time:** ~17h on 1x H100, ~2.5h on 8x H100 (500 epochs). 100 epochs is sufficient for good results.

The training uses a rectified flow loss formulation with logit-normal timestep sampling, conditioning on the first two video frames.

### 5. Run inference

```bash
export LORA_DIR="output/cosmos_lora"
export DATA_DIR="gr1_dataset/test"
export OUT_DIR="output/eval_videos"

python eval_cosmos_predict25_lora.py \
  --data_dir $DATA_DIR \
  --output_dir $OUT_DIR \
  --lora_dir $LORA_DIR \
  --height 432 --width 768 \
  --num_output_frames 93 \
  --num_steps 36 \
  --seed 0
```

Or generate videos programmatically:

```python
from diffusers import Cosmos2_5_PredictBasePipeline
from diffusers.utils import load_image, export_to_video
import torch

pipe = Cosmos2_5_PredictBasePipeline.from_pretrained(
    "nvidia/Cosmos-Predict2.5-2B",
    revision="diffusers/base/post-trained",
    device_map="cuda",
    torch_dtype=torch.bfloat16,
)
pipe.load_lora_weights("/path/to/lora/checkpoint")
pipe.fuse_lora(lora_scale=1.0)

image = load_image("input.png")
prompt = "Use the left hand to pick up dark green cucumber"

frames = pipe(
    image=image,
    prompt=prompt,
    num_frames=93,
    num_inference_steps=36,
    height=432,
    width=768,
).frames[0]

export_to_video(frames, "output.mp4", fps=16)
```

### 6. Evaluate quality

Two evaluation approaches:

- **Sampson Error**: Measures geometric consistency (temporal within frames, cross-view alignment). Lower is better.
- **LLM-as-Judge (Cosmos Reason2)**: Scores physical plausibility and instruction following on a 1-5 scale using rubrics in `llm_judge_prompts/video_physics.yaml` and `llm_judge_prompts/video_IF.yaml`.

Key findings: LoRA r=32 significantly improves instruction following (correct hand usage, object interactions) while preserving geometric and physical priors from the frozen base model.

## References

- [Blog post: Fine-Tuning NVIDIA Cosmos Predict 2.5 with LoRA/DoRA](https://huggingface.co/blog/nvidia/cosmos-fine-tuning-for-robot-video-generation)
- [Training code (Diffusers example)](https://github.com/terarachang/diffusers/tree/cosmos_predict_2.5_lora_clean/examples/cosmos)
- [Cosmos Cookbook](https://nvda.ws/4qevli8)
- [NVIDIA Cosmos on Hugging Face](https://huggingface.co/nvidia/collections?search=cosmos)
- [NVIDIA Cosmos GitHub](https://github.com/nvidia-cosmos)
