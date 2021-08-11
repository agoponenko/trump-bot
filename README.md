# Service with dialog model fine-tuned to be pretending Donald Trump

This is a placeholder with dialog model fine-tuned to dialogs with Donald Trump and based on 
[DialoGPT](https://github.com/microsoft/DialoGPT) model.
Despite new SOTA solutions in conversational AI like Meena or Blender, DialoGPT was chosen here as 
it does not require several GPUs to be trained, and it became pretty common in domain.

## Description of solution (step-by-step)

### 1. Data.
Data was downloaded from the following pages:
1. https://www.rev.com/blog/transcript-tag/donald-trump-interview-transcripts
2. https://www.kaggle.com/mrisdal/2016-us-presidential-debates
3. https://www.kaggle.com/headsortails/us-election-2020-presidential-debates/version/7
### 2. Data preprocessing, preparing datasets.
Downloaded data is transformed to context windows, so that current phrase and 7 previous phrases 
are used in training and validation data. About training and validation datasets: 
simple train_test_split with 0.85/0/15 ratio is used. Shuffle is True per default.
### 3. Model architecture.
The intent behind DialoGPT (GPT-2) is that it gives pretty good results in generating 
text sequences, as core Transformer-based model was trained on huge amount of comments from Reddit, 
which is pretty good dataset to simulate communication on the internet 
(what we need in this project). 
There are 3 DialoGPT models with different number of parameters, 
small DialoGPT 117M model was used in this project due to computational resources problem.
### 4. Training and evaluation.
Model is fine-tuned, so we do not train one from scratch. Train loop includes 3 epochs.
Fine-tuning was performed with the help of Google Colab. You can find training notebook, 
as well as training data here via [the link](https://drive.google.com/drive/folders/1YU2igVUUQ0FTJcfo8iMG1yM51AYab4kW?usp=sharing).

### References
The training scripts and model configuration is mostly based on 
[this great tutorial](https://nathancooper.io/i-am-a-nerd/chatbot/deep-learning/gpt2/2020/05/12/chatbot-part-1.html).


### Running
```
python run.py
```


https://user-images.githubusercontent.com/27633882/129045854-0c6e6b09-daaa-4c49-acc3-ed8897d39e09.mov



## Results
Just simple dialog model was trained, which is not perfect. 
With more data and GPUs it can be significantly improved. Also, 
postprocessing outputs of model can improve quality of answers (but in another iteration). 
For example, put Trump / non-Trump classifier on top of dialog model will adjust outputs more precisely.
