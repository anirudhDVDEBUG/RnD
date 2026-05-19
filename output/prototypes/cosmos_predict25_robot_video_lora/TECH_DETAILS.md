# Technical Details: Cosmos Predict 2.5 LoRA Fine-Tuning

## What It Does

Cosmos Predict 2.5 is NVIDIA's 2B-parameter world foundation model that generates video from an image and text prompt. This technique fine-tunes it with LoRA (Low-Rank Adaptation) adapters on a small dataset of 92 robot manipulation videos (GR1-100) so the model learns to follow specific robotic task instructions -- which hand to use, which object to manipulate, and what action to perform. The base model already understands physics and geometry; LoRA teaches it the domain-specific instruction-following behavior while keeping all base knowledge frozen.

The key insight is that only ~2.5% of parameters need training (~50M out of 2B) to achieve a dramatic improvement in instruction following (from ~2/5 to ~4/5 on LLM-judge scores), while geometric consistency and physical plausibility remain intact or slightly improve.

## Architecture

### Model Components
- **DiT (Diffusion Transformer):** The core 2B-parameter video generation backbone. LoRA adapters are attached to its attention (`to_q`, `to_k`, `to_v`, `to_out.0`) and feedforward (`ff.net.0.proj`, `ff.net.2`) layers.
- **VAE:** Encodes/decodes video frames to/from latent space. Frozen during training.
- **T5 Text Encoder:** Converts text prompts to conditioning embeddings. Frozen during training.

### Data Flow
```
Input Image + Text Prompt
    |
    v
T5 Encoder --> text embeddings (frozen)
VAE Encoder --> latent frames (frozen)
    |
    v
DiT with LoRA adapters (trainable)
  - Rectified flow loss with logit-normal timestep sampling
  - Conditions on first 2 frames (input image duplicated)
    |
    v
VAE Decoder --> generated video frames (frozen)
    |
    v
MP4 output (93 frames @ 16fps = 5.8s)
```

### Training Details
- **Loss:** Rectified flow formulation -- the model learns to predict the velocity field that transforms noise into the target video latent. Uses logit-normal timestep sampling which biases toward intermediate timesteps where the signal-to-noise ratio is most informative.
- **Conditioning:** The first two frames are always the input image (duplicated), so the model generates a continuation from a single starting frame.
- **LoRA mechanics:** Each target layer gets a low-rank decomposition `W + BA` where `B` is rank x hidden_dim and `A` is hidden_dim x rank. Only `A` and `B` are trained. DoRA adds a learnable magnitude vector for better training stability.

### Dependencies
- `diffusers` >= 0.32.0 (Cosmos pipeline support)
- `peft` >= 0.14.0 (LoRA/DoRA implementation)
- `accelerate` (distributed training, mixed precision)
- `transformers` (T5 text encoder)
- `torch` >= 2.5 with CUDA (bf16, tf32 support)

### Key Files (in training repo)
- `train_cosmos_predict25_lora.py` -- Training script with rectified flow loss
- `eval_cosmos_predict25_lora.py` -- Batch inference on test set
- `download_and_preprocess_datasets.sh` -- Dataset download and formatting
- `llm_judge_prompts/video_physics.yaml` -- Physics plausibility rubric
- `llm_judge_prompts/video_IF.yaml` -- Instruction following rubric

## Limitations

- **Hardware:** Requires minimum 80GB VRAM (A100/H100). Multi-GPU recommended for practical training times.
- **Dataset scope:** Trained on 92 GR1-100 videos of tabletop manipulation. Does not generalize to arbitrary robot morphologies, outdoor scenes, or non-manipulation tasks without additional data.
- **Resolution:** Fixed at 432x768. Higher resolutions require model architecture changes.
- **Video length:** 93 frames (~5.8s). Longer videos need autoregressive extension or model modifications.
- **No real-time inference:** Each video takes minutes to generate on a single GPU (36 denoising steps through the full DiT).
- **Evaluation:** LLM-as-Judge scores depend on the judge model (Cosmos Reason2) and rubric design. Sampson error only measures geometric consistency, not semantic correctness.

## Why It Matters for Claude-Driven Products

**Synthetic training data for robotics:** Claude agents orchestrating robot fleets could use Cosmos to generate simulated training videos for new tasks before physical deployment -- reducing sim-to-real gaps.

**Video content generation:** Marketing and ad-creative pipelines could use fine-tuned video generation to produce product manipulation demos (unboxing, assembly, usage) from a single product photo and text description.

**Agent factories:** A Claude-based agent factory could fine-tune Cosmos adapters on-demand for new domains (warehouse picking, kitchen tasks, surgical robots) by collecting a small video dataset and launching LoRA training -- the 2.5-hour turnaround on 8x H100 is fast enough for iterative development.

**Evaluation infrastructure:** The dual evaluation approach (geometric metrics + LLM-as-Judge) is a reusable pattern for any video generation quality assessment pipeline, applicable beyond robotics.
