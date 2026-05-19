# How to Use: Cosmos Predict 2.5 LoRA Fine-Tuning

## Install

```bash
# Python 3.10+, PyTorch 2.5+ with CUDA required
pip install -U "diffusers[torch]" transformers accelerate peft wandb safetensors opencv-python

# Clone the training scripts
git clone -b cosmos_predict_2.5_lora_clean https://github.com/terarachang/diffusers.git cosmos-diffusers
cd cosmos-diffusers/examples/cosmos
```

**Hardware:** Minimum 1x 80GB GPU (A100/H100). 8x H100 recommended for fast training.

## First 60 Seconds

Run the demo (no GPU needed):

```bash
bash run.sh
```

This creates a mock dataset, shows the LoRA configuration, simulates training, and prints a comparison table of base vs fine-tuned evaluation metrics. Output is written to `output/demo_results.json`.

## Full Training Pipeline

### 1. Prepare the dataset

Download the GR1-100 (92 training videos) and GR00T-Eval (50 test pairs):

```bash
# From the cosmos-diffusers/examples/cosmos directory:
bash download_and_preprocess_datasets.sh
```

This creates:
```
gr1_dataset/
  train/
    metas/*.txt       # text prompts per video
    videos/*.mp4      # robot manipulation videos
    metadata.csv      # video_path,prompt_path mapping
  test/
    *.txt             # test prompts
    *.png             # conditioning images (first frame)
```

Datasets: [nvidia/GR1-100](https://huggingface.co/datasets/nvidia/GR1-100), [nvidia/PhysicalAI-Robotics-GR00T-Eval](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-Eval).

### 2. Train

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

Add `--use_dora` for the DoRA variant. 100 epochs is sufficient for good results; 500 is the full run.

**Training time:** ~17h on 1x H100, ~2.5h on 8x H100.

### 3. Run inference

```bash
python eval_cosmos_predict25_lora.py \
  --data_dir gr1_dataset/test \
  --output_dir output/eval_videos \
  --lora_dir output/cosmos_lora \
  --height 432 --width 768 \
  --num_output_frames 93 \
  --num_steps 36 \
  --seed 0
```

Or programmatically:

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
pipe.load_lora_weights("output/cosmos_lora")
pipe.fuse_lora(lora_scale=1.0)

image = load_image("input.png")
prompt = "Use the left hand to pick up dark green cucumber"

frames = pipe(
    image=image, prompt=prompt,
    num_frames=93, num_inference_steps=36,
    height=432, width=768,
).frames[0]

export_to_video(frames, "output.mp4", fps=16)
```

### 4. Evaluate

Two complementary metrics:

- **Sampson Error:** Geometric consistency between frames. Run with OpenCV keypoint matching.
- **LLM-as-Judge (Cosmos Reason2):** Scores physical plausibility (1-5) and instruction following (1-5) using rubrics in `llm_judge_prompts/`.

## Configuration Reference

See `cosmos_lora_config.py` for all hyperparameters. Key choices:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `lora_rank` | 32 | Best quality. Use 8 for memory-constrained setups |
| `lora_alpha` | 32 | Equal to rank for scale factor 1.0 |
| `use_dora` | False | Enable if training is unstable |
| `num_train_epochs` | 500 | 100 is sufficient for good results |
| `height x width` | 432x768 | Native resolution for Cosmos 2.5 |
| `num_output_frames` | 93 | ~5.8s at 16fps |
