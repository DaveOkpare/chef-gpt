# ChefGPT

This is a web app that generates recipes from pictures of grocery items. You can upload an image of the ingredients you have and the app will use a LLM model to create a recipe for you. 

### How to use

To use this app, you need to obtain API keys from OpenAI and Replicate. You can sign up for [OpenAI](https://platform.openai.com/) and for [Replicate](https://replicate.com/). Once you have the keys, you need to set them as environment variables or add them to a `.env` file:

```shell
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export REPLICATE_API_TOKEN=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Then, you can run the app locally using Streamlit:

```shell
pip install streamlit
streamlit run app.py
```

Alternatively, you can deploy the app to a cloud platform of your choice, such as HuggingFace Spaces or AWS.
