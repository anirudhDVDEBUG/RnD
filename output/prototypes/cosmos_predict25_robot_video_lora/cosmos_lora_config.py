"""
Configuration for Cosmos Predict 2.5 LoRA/DoRA fine-tuning.
Defines model, training, and LoRA hyperparameters.
"""

MODEL_NAME = "nvidia/Cosmos-Predict2.5-2B"
MODEL_REVISION = "diffusers/base/post-trained"

# LoRA configuration
LORA_CONFIG = {
    "r": 32,                 # Rank: 32 recommended, 8 for memory-constrained
    "lora_alpha": 32,        # Set equal to rank for scale factor 1.0
    "target_modules": [
        "to_q", "to_k", "to_v", "to_out.0",  # Attention layers
        "ff.net.0.proj", "ff.net.2",           # Feedforward layers
    ],
    "use_dora": False,       # Set True for DoRA (magnitude decomposition)
}

# Training configuration
TRAIN_CONFIG = {
    "train_batch_size": 1,
    "num_train_epochs": 500,
    "checkpointing_epochs": 100,
    "learning_rate": 1e-4,
    "mixed_precision": "bf16",
    "seed": 0,
    "height": 432,
    "width": 768,
    "num_frames": 93,
    "allow_tf32": True,
    "gradient_checkpointing": True,
}

# Inference configuration
INFERENCE_CONFIG = {
    "num_output_frames": 93,
    "num_inference_steps": 36,
    "height": 432,
    "width": 768,
    "fps": 16,
    "seed": 0,
    "lora_scale": 1.0,
}

# Dataset paths
DATASET_PATHS = {
    "train_dir": "gr1_dataset/train",
    "test_dir": "gr1_dataset/test",
    "train_videos": "gr1_dataset/train/videos",
    "train_metas": "gr1_dataset/train/metas",
    "train_metadata_csv": "gr1_dataset/train/metadata.csv",
}

# Evaluation rubrics
EVAL_CONFIG = {
    "sampson_error": True,          # Geometric consistency metric
    "llm_judge": True,              # Cosmos Reason2 scoring
    "physics_rubric": "llm_judge_prompts/video_physics.yaml",
    "instruction_following_rubric": "llm_judge_prompts/video_IF.yaml",
}
