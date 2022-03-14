# Deployment of the executable REST web service
from flask import *
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    try :
        input_sentence = request.args.get('text') # get input from URL
        if input_sentence == None or  input_sentence.replace(' ', '') == '' :
            return jsonify({'error':'No text parameter provided'})
        input_sentence = str (input_sentence)
        #Text cleaning by regex to replace all bits except arabic letters by spaces
        #remove [ English letters , numbers , special characters , ... ] as They not affect on The dialect
        import re
        match = r'[^\u0020\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+'
        input_sentence = re.sub(match ,' ', input_sentence)
        
        input_sentence = ' '.join(input_sentence.split()) #replace spaces by only 1 space
        
        import pandas
        data_set = pandas.read_csv("dialect_dataset_cleaned.csv",encoding ='utf-16')
        
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        
        tokenizer = Tokenizer(num_words = 600000, oov_token="<OOV>")
        tokenizer.fit_on_texts( list(map(str, data_set['text']) ) )
        
        input_sentence = tokenizer.texts_to_sequences([input_sentence])
        input_sentence = pad_sequences(input_sentence, padding='post', maxlen=80)
        
        import joblib
        model = joblib.load('joblib.sav')
        
        from numpy.ma.core import argmax
        from sklearn.preprocessing import LabelEncoder
        encoder = LabelEncoder().fit(data_set['dialect'])
        
        predict = model.predict(input_sentence) #vector[18]
                
        return jsonify({'dialect'     : str ( encoder.inverse_transform ([ argmax(predict) ]) [0] ) ,
                        'probability' : str ( max( predict[0] ) ) })
    except:
        return jsonify({'error':'true'})

if __name__ == '__main__':
    app.run(debug=True)