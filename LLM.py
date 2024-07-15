 
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def model_inference(content,companies):

    model_id = "meta-llama/Llama-2-7b-hf"
    #print("model_id: ", model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id,token ="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")
    #print("tokenizer: ", tokenizer)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="cpu", token = "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"
    )
    prompt = 'extract from the input text the The size of the equity checks they are writing for solarpark investments. If no information is available, output "N/A". The total megawatts of solarparks they are investing in. If no information is available, output "N/A".Investment in Solarparks: For each company, indicate whether they are investing in solarparks. Output a boolean value (true or false) for each company. If no information is available, output "N/A".The companies are:{companies}'

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": content},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    print(tokenizer.decode(response, skip_special_tokens=True))
