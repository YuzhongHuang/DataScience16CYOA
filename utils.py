# functions definition for length data operation

def createLowerWordList(line):
    """
    Given a line of string, seperates 
    the string into lower case word and
    get rid of punctuations and numbers
    """
    # get a splited words list and an empty list
    wordList1 = line.split()
    wordList2 =[]
    # loop through the word list to get rid of punctuations and convert words to lower case
    for word in wordList1:
        cleanWord = ""
        for char in word:
            if char in '!,.?":;0123456789':
                char = ""
            cleanWord += char
        cleanWord = cleanWord.lower()
        if cleanWord != "":
            wordList2.append(cleanWord)
    return wordList2

def add_length(df):
    """
    Generates a length column for given dataset
    to describe each phrase's length
    """
    length = lambda x: len(createLowerWordList(x))
    df['Length'] = df['Phrase'].apply(length)
    
def add_whole_sentence(df):
    """
    Generates a boolean 'WholeSentence' column for given dataset
    to indicate whether the phrase is a whole sentence or not
    """
    df['WholeSentence'] = False
    # initialize a last_id for comparison
    last_id = 0
    # loop throught the dataframe to set the first sentence for each sentence group's 'WholeSentence' to be True
    for index, row in df.iterrows():
        # changes 'WholeSentence' to be true for the first sentence for each sentence group
        if last_id != row['SentenceId']:
            last_id = row['SentenceId']
            df.set_value(index, 'WholeSentence', True)
            
def get_average_length_sentiment(df):
    """
    create a dataframe by seperating the data by sentiment
    and compute the mean for the length
    """
    dict = {}
    # sentiment_max stores the value of maxium sentiment, which is 4 in this case
    sentiment_max = 4
    # loop through sentiment and compute the length for the data
    # and store its mean and standard deviation to the dictionary
    for i in range(sentiment_max + 1):
        length_series = df[df['Sentiment'] == i]['Length']
        dict[i] = [length_series.mean(), length_series.std()]
    # convert the dictionary to a dataframe
    length_df = pd.DataFrame(dict.items(), columns=['Sentiment', 'Mean_Std'])
    length_df['AverageLength'] = length_df['Mean_Std'].apply(lambda x: x[0])
    length_df['Std'] = length_df['Mean_Std'].apply(lambda x: x[1])
    return length_df

# functions definition for length data operation
def createLowerWordList(line):
    """
    Given a line of string, seperates 
    the string into lower case word and
    get rid of punctuations and numbers
    """
    # get a splited words list and an empty list
    wordList1 = line.split()
    wordList2 =[]
    # loop through the word list to get rid of punctuations and convert words to lower case
    for word in wordList1:
        cleanWord = ""
        for char in word:
            if char in '!,.?":;0123456789':
                char = ""
            cleanWord += char
        cleanWord = cleanWord.lower()
        if cleanWord != "":
            wordList2.append(cleanWord)
    return wordList2

def add_length(df):
    """
    Generates a length column for given dataset
    to describe each phrase's length
    """
    length = lambda x: len(createLowerWordList(x))
    df['Length'] = df['Phrase'].apply(length)
    
def add_whole_sentence(df):
    """
    Generates a boolean 'WholeSentence' column for given dataset
    to indicate whether the phrase is a whole sentence or not
    """
    df['WholeSentence'] = False
    # initialize a last_id for comparison
    last_id = 0
    # loop throught the dataframe to set the first sentence for each sentence group's 'WholeSentence' to be True
    for index, row in df.iterrows():
        # changes 'WholeSentence' to be true for the first sentence for each sentence group
        if last_id != row['SentenceId']:
            last_id = row['SentenceId']
            df.set_value(index, 'WholeSentence', True)

def get_average_length_sentiment(df):
    """
    create a dataframe by seperating the data by sentiment
    and compute the mean for the length
    """
    dict = {}
    # sentiment_max stores the value of maxium sentiment, which is 4 in this case
    sentiment_max = 4
    # loop through sentiment and compute the length for the data
    # and store its mean and standard deviation to the dictionary
    for i in range(sentiment_max + 1):
        length_series = df[df['Sentiment'] == i]['Length']
        dict[i] = [length_series.mean(), length_series.std()]
    # convert the dictionary to a dataframe
    length_df = pd.DataFrame(dict.items(), columns=['Sentiment', 'Mean_Std'])
    length_df['AverageLength'] = length_df['Mean_Std'].apply(lambda x: x[0])
    length_df['Std'] = length_df['Mean_Std'].apply(lambda x: x[1])
    return length_df

# functions definition for sentence data operation
def create_sentence_df(df):
    """
    sentence_df() groups phrases with same 
    Sentence Id and returns a dataframe with
    each groups's whole sentence's sentiment,
    the phrases' sentiment's standard deviation
    and variance
    """
    # dictionary to store values collected from sentence group
    sentence_dict = {}
    # loop through dataframes with the same sentence ID
    for i in range(df['SentenceId'].max()):
        # select data with sentence ID i
        select_df = df[df['SentenceId'] == i]
        # internally drop Nan data
        if not select_df.empty:
            # store a list with the structure "[overall_sentiment, variance, standard deviation]"
            sentence_dict[i] = [select_df.iloc[0, 3], select_df['Sentiment'].var(), select_df['Sentiment'].std(), select_df.iloc[0, 4]]
    # convert dictionary to pandas dataframe
    sentence_df = pd.DataFrame(sentence_dict.items(), columns=["Sentence", "Sentiment_Var_Std_Length"])
    
    # split the 'Sentiment_Var_Std' column to 'Sentiment', 'Var', 'Std'
    sentence_df['Sentiment'] = sentence_df['Sentiment_Var_Std_Length'].apply(lambda x: x[0])
    sentence_df['Var'] = sentence_df['Sentiment_Var_Std_Length'].apply(lambda x: x[1])
    sentence_df['Std'] = sentence_df['Sentiment_Var_Std_Length'].apply(lambda x: x[2])
    sentence_df['Length'] = sentence_df['Sentiment_Var_Std_Length'].apply(lambda x: x[3])
        
    return sentence_df.drop('Sentiment_Var_Std_Length', axis=1)

def create_word_df(df):
    """
    Create a dataframe documenting the frequency, standard deviation and 
    mean value of each unique word appears in the given dataframe  
    """
    word_dict = {}
    for index, row in df.iterrows():
        list = createLowerWordList(row["Phrase"])
        sentiment = row["Sentiment"]
        
        for word in list:
            if word in word_dict:
                word_dict[word][0] += 1
                word_dict[word][1].append(sentiment)
            else:
                word_dict[word] = [1, [sentiment]]
    
    word_df = pd.DataFrame(word_dict.items(), columns=["Word", "Frequency-Sentiment"])
    word_df['Frequency'] = word_df['Frequency-Sentiment'].apply(lambda x: x[0])
    word_df['Sentiment'] = word_df['Frequency-Sentiment'].apply(lambda x: np.mean(x[1]))
    word_df['Std'] = word_df['Frequency-Sentiment'].apply(lambda x: float(np.std(x[1])))
    return word_df.drop('Frequency-Sentiment', 1).dropna().sort_values(['Frequency'], ascending=False)

def sentiment_std_zero_length_plot(sentiment):
    """
    takes a given sentiment value, plot the distribution
    of length of std_0 group against std_non_0 group of 
    the given sentiment value group
    """
    # distibution plot of std_0 group
    sns.distplot(sentence_df[(sentence_df['Sentiment'] == sentiment) & (sentence_df['Std_zero'] == True)].Length, 
                 kde_kws={"color": "g", "lw": 3, "label": "Std_zero"})
    # distibution plot of std_non_0 group
    sns.distplot(sentence_df[(sentence_df['Sentiment'] == sentiment) & (sentence_df['Std_zero'] == False)].Length, 
                 kde_kws={"color": "r", "lw": 3, "label": "Std_non_zero"})