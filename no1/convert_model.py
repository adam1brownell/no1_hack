import coremltools as ct
import onnx

# Path to your downloaded ONNX model file
onnx_model_path = "/Users/adambrownell/passion_projects/no1_hack/no1/models/phi3-mini-4k-instruct-cpu-int4-rtn-block-32-acc-level-4.onnx"
# Output path for the CoreML model
coreml_model_output_path = "/Users/adambrownell/passion_projects/no1_hack/no1/src/no1/resources/phi3_mini_4k_instruct.mlmodel"

# Load the ONNX model
onnx_model = onnx.load(onnx_model_path)

# Convert the ONNX model to CoreML
mlmodel = ct.converters.onnx.convert(
    model=onnx_model_path,  # Load the ONNX model
    minimum_ios_deployment_target='13',  # Set the minimum iOS version
    compute_precision=ct.precision.FLOAT16  # Optional: convert to 16-bit float to reduce model size
)

# Add metadata (optional but recommended)
mlmodel.short_description = "Phi-3 Mini-4K-Instruct conversational model"
mlmodel.input_description["input"] = "Input token ids for text processing"
mlmodel.output_description["output"] = "Generated text"

# Save the CoreML model
mlmodel.save(coreml_model_output_path)

print(f"Model saved to {coreml_model_output_path}")
