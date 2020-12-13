Please keep below files (part of Zipped file) at some local path <Localpath>- 

1. Term_Extraction_Project.py - This is module version of our project code.
2. corpusPath.txt  - contains path to corpus of all 3 domains
   Content of this file "corpusPath.txt"- 
 	<Localpath>\Domains\Banking\Corpus
	<Localpath>\Domains\Jyotish\Corpus
	<Localpath>\Domains\Vamaniki\Corpus
Kindly replace <LocalPath> with appropraite path in corpusPath.txt before running the program.


3. hindi_stop_words.txt - contains hindi stop words, being used in our program
4. Domains.txt - contains Domain names in same order as of Domain corpus path stored in above "corpusPath.txt" file.
   Content of this file "Domains.txt"

5. Keep "Domains" folder (you will get it after unzipping the main file), so folder structure will be same of the path mentioned in   "corpusPath.txt"

	<Localpath>\Domains\Banking\Corpus
	<Localpath>\Domains\Jyotish\Corpus
	<Localpath>\Domains\Vamaniki\Corpus

were <Localpath> will be the path where you are keeping all the above listed files.

****Command to run the module - In command prompt, go to <Localpath>src where you have kept above files and run below command - 

python Term_Extraction_Project.py ./corpusPath.txt ./hindi_stop_words.txt ./Domains.txt

Output Format - Output file will be generated at same <localpath>
Outfilename - Codeoutput.txt

Implementation Limitation - 

1. It needs POS tagged corpus for 3 domains as of now.
2. Code can run for only 3 domains as of now, however it can be generalized later to run for as many as domains we will pass in program.
3. Sequence of Domain name and Domain Corpus path will be same in "Domains.txt" and ""corpusPath.txt"" respectively.
4. This implementation requires POS tagged corpus.


Data Collection:

We collected data from hindi wikipedia and used an online POS tagger. Tool used for this was Selenium.


Team Member Contribution

Rahul : Tagged Corupus Collection and NCI NDI implementation
Suraj : POS taggger for Hindi, Data Cleaning and Lingustic Filter, Read me file
Arvin : Research paper sorting and finalization,Stemming for Hindi and Stop Word removal, Presentation




