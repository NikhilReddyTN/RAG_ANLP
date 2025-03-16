# CMU Advanced NLP Assignment 2

Directory Structure:

1. data: contains all our scraped data in JSON format

2. input: contains additional pdf files used to scrape data

3. scraping_code: contains the various scripts used to scrape from websites and documents

4. rag.py: contains the code for the rag system

5. login.py: contains code to store hugging face api key

6. questions.csv: The questions you want to generate answers for

7. Total data annotations: questions.txt, questions_2.txt

8. Test data annotations: selected_questions.txt



Instructions to Run the RAG System:

1. Run the login.py file and enter huggin face api key when prompted. (Create a read only api key in hugging face and accept terms and conditions for open source use of the llama model)

2. Add the questions to the questions.csv file.

3. Run the rag.py file

The answers will be generated to answers.json