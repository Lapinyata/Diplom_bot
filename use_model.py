import pickle
from clean_user_news import main_cleaner

async def predict_news(text):
  final_text = main_cleaner(text)
  rf_clf_model = pickle.load(open('final_rf_ppl_clf.sav', 'rb'))
  predict = rf_clf_model.predict_proba([final_text])
  return predict[0][1]