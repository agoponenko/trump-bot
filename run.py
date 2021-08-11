from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small', use_fast=False)
model = AutoModelForCausalLM.from_pretrained('output-small')

for step in range(100):
    # Encode the new user input, add the eos_token and return a tensor in PyTorch.
    new_user_input_ids = tokenizer.encode(input(">> User: ") + tokenizer.eos_token,
                                          return_tensors='pt')

    # Append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # Generated a response while limiting the total chat history to 1000 tokens
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=100,
        top_p=0.7,
        temperature=0.8
    )

    # Pretty print last output tokens from bot
    print("Donal Trump: {}".format(tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))