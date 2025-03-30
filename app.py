import gradio as gr
import time # Placeholder for simulating work
import os
from pathlib import Path
import uuid  # For unique job directories
import shutil # For file copying

# --- Main Training Function (Replaces Placeholder) ---

def run_training_job(style_name, base_model, training_steps, learning_rate, image_files):
    job_id = str(uuid.uuid4())
    print(f"--- Starting Training Job {job_id} ---")
    print(f"Style Name: {style_name}")
    print(f"Base Model: {base_model}")
    print(f"Training Steps: {training_steps}")
    print(f"Learning Rate: {learning_rate}")
    print(f"Number of images: {len(image_files) if image_files else 0}")

    # --- Input Validation ---
    if not style_name:
        yield "Error: Please provide a Style/Concept Name.", None
        return
    if not image_files:
        yield "Error: No images uploaded.", None
        return
    
    # --- Prepare Data Directory ---
    job_data_dir = Path(f"data/{job_id}")
    instance_images_dir = job_data_dir / "images"
    try:
        instance_images_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created job data directory: {instance_images_dir}")

        # Copy uploaded images to the job directory
        yield "Processing uploaded images...", None
        for img_file in image_files:
            # Gradio Files component provides objects with a .name attribute (temp path)
            temp_path = img_file.name
            # Create a destination path inside the instance_images_dir
            # Use the original filename from the temp path
            dest_path = instance_images_dir / Path(temp_path).name
            shutil.copy2(temp_path, dest_path) # copy2 preserves metadata if possible
            print(f"Copied {temp_path} to {dest_path}")
        
        yield f"Image preparation complete. {len(image_files)} images ready.", None

    except Exception as e:
        error_message = f"Error preparing data directory: {e}"
        print(error_message)
        # Attempt cleanup if directory creation partially succeeded
        if job_data_dir.exists():
            shutil.rmtree(job_data_dir)
        yield error_message, None
        return

    # --- Placeholder for Step 5: Subprocess Execution --- 
    # At this point, instance_images_dir contains the images needed for training.
    # We would now construct and run the subprocess command.
    
    # Simulate training progress (keeping the dummy logic for now)
    yield "Starting placeholder training simulation...", None 
    total_steps = int(training_steps)
    for i in range(total_steps):
        time.sleep(0.01) # Simulate work
        if (i + 1) % (total_steps // 10) == 0 or i == total_steps - 1: # Update roughly 10 times + final
             yield f"Training progress: {i + 1}/{total_steps} steps", None
    
    # Simulate completion and provide a dummy file path (using job_id)
    dummy_model_dir = Path("models")
    dummy_model_path = dummy_model_dir / f"{job_id}_{style_name}_model.safetensors"
    
    try:
        dummy_model_dir.mkdir(parents=True, exist_ok=True)
        with open(dummy_model_path, 'w') as f:
            f.write(f"Placeholder for job {job_id}\n")
        print(f"Created dummy file at: {dummy_model_path}")
        yield f"Training finished! Model saved (placeholder).", str(dummy_model_path)
    except Exception as e:
        error_message = f"Error creating dummy file: {e}"
        print(error_message)
        yield error_message, None
        # Attempt cleanup of data dir if dummy file creation failed
        if job_data_dir.exists():
             shutil.rmtree(job_data_dir)
        return
    # --- End Placeholder --- 

# --- Gradio Interface Definition ---

# Define choices for base models
base_model_choices = [
    "runwayml/stable-diffusion-v1-5", 
    "stabilityai/stable-diffusion-xl-base-1.0",
    # Add more common models here if desired
]

# Use Blocks for more layout control
with gr.Blocks() as iface:
    gr.Markdown("# Style Assimilator")
    gr.Markdown("Upload a few sample images of your style/concept and generate a LoRA model.")

    with gr.Row():
        with gr.Column(scale=1):
            # Inputs
            style_name = gr.Textbox(label="Style/Concept Name", placeholder="e.g., MyArtisticStyle or CuteRobots")
            base_model = gr.Dropdown(label="Base Model", choices=base_model_choices, value=base_model_choices[0])
            
            with gr.Row():
                 max_train_steps = gr.Number(label="Training Steps", value=1000, minimum=100, step=50)
                 learning_rate = gr.Number(label="Learning Rate", value=1e-4, minimum=1e-6, maximum=1e-3, step=1e-6, info="e.g., 1e-4 or 0.0001")
                 # Potential future additions: resolution, rank, batch_size etc.

            image_uploader = gr.Files(label="Upload Sample Images (5-20 recommended)", file_types=["image"]) 
            
            start_button = gr.Button("Start Training", variant="primary")

        with gr.Column(scale=1):
            # Outputs
            status_output = gr.Textbox(label="Status / Logs", lines=10, interactive=False)
            model_output = gr.File(label="Download Trained LoRA Model", interactive=False)

    # Connect button click to the *new* function name
    start_button.click(
        fn=run_training_job, # <-- Updated function name
        inputs=[style_name, base_model, max_train_steps, learning_rate, image_uploader],
        outputs=[status_output, model_output]
    )

# --- Launch the Interface ---
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0") # Run on all interfaces within Docker 