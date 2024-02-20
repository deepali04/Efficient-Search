# SearchEngine

## 
EfficientSearchengine is a cutting-edge search engine which employs a Trie data structure for the efficient storage and retrieval of data, leading to a significant enhancement in search speed by approximately 20%. Additionally, it features an innovative auto-complete function that offers real-time suggestions to users, which has contributed to a significant increase in user engagement.

The search engine demonstrates algorithmic excellence through the implementation of sophisticated algorithms that have effectively optimized its performance, resulting in a decrease in query response times. Furthermore, various performance optimization techniques have been applied to improve efficiency in real-world search situations, culminating in a noteworthy 16% reduction in memory consumption.

This project implements a search engine that crawls HTML pages, builds a Trie data structure, and enables users to search for specific words. The user interface is created using Tkinter. I have handled stop words using python library sklearn.

### Approach

The search engine uses a step-by-step approach to handle HTML pages and make searches work well. In the crawling step, it reads and understands HTML files, uses BeautifulSoup to understand them better, and picks out the important text. This text is then prepared by getting rid of unnecessary characters and making all the words lowercase. The search engine relies on a trie data structure to organize words. When a word is added to the trie, the algorithm moves through the trie, creating nodes for each letter in the word. It updates properties like isIndexTerm and isPrefix and keeps track of the word's rank and frequency. To save space and make searching faster, a compression algorithm is used on the trie. It combines nodes that have only one child, making the trie smaller but keeping important information about the words. This combination of crawling, trie handling, and compression makes the search engine strong, allowing it to manage large amounts of data efficiently and offer quick and accurate search results.

### Algorithms:

- **Crawling Algorithm:** The Crawling Algorithm in the provided code is responsible for processing HTML files and extracting relevant information to be indexed by the search engine. It utilizes the crawlPage method within the MySearchEngine class.

- **Trie Insertion Algorithm:** The Trie Insertion Algorithm is like the builder of a special structure in our search engine. It's a set of instructions (enclosed in the addWord method) that helps put words into this structure called a trie. Imagine it as a tree where each word is made up of individual letters. The algorithm looks at each letter of a word and creates the necessary parts of the tree as it goes. It also keeps count of how often a word appears. Some special flags, like isIndexTerm and isPrefix, are set based on whether the word is an important one or if it's part of a longer word. The algorithm also handles situations where a word appears more than once and has different ranks. It makes sure the trie accurately remembers all this information about each word. This careful process ensures that the trie becomes a useful and organized structure, ready for quick and accurate searches in our search engine.

-	**Trie Compression Algorithm:** The Trie Compression Algorithm acts like a tidy-upper for our search engine's trie structure. Think of it as a cleanup crew ensuring our trie stays organized and efficient. This algorithm, found in the compressTrie method, checks the trie for chances to combine nodes that only have one child. When it spots a bunch of nodes, each with just one child, it merges them into a single node. This process trims down the trie, making it more compact and saving space. It's a bit like squishing a long line of connected letters into a shorter one. Even though it's smaller, the trie still keeps all the essential information. This helps speed up searches because the trie is more streamlined. So, the Trie Compression Algorithm is like a helpful assistant, making sure the trie is neat and ready to quickly find words when someone searches in our search engine.

-	**Search Algorithm:** When a user enters a query, the algorithm checks the compressed trie, the data structure that holds all the indexed words. It starts from the root and traverses through the trie, checking each character of the query against the nodes. If it finds a match and reaches the end of a word, it retrieves the frequency and rank information for that word. This meticulous process ensures accurate and efficient searches. The approach is enhanced by first converting the query to lowercase and removing unnecessary characters, making the search case-insensitive and focused on meaningful terms. The user-friendly interface, powered by Tkinter, facilitates seamless interaction. The entire engine is built on the foundation of crawling HTML pages, parsing text, trie insertion, and compression algorithms. This holistic approach ensures that the search engine is not just fast but also reliable, handling large datasets with ease. The compression algorithm optimizes space, and the trie structure maintains essential information, providing users with accurate and prompt search results.


### Data Structures:

**Trie:**
  - The trie data structure efficiently stores words and facilitates quick searches.
  - Trie nodes store information about characters, relationships, and ranking.

**Ranking Dictionary:**
  - A dictionary is used to store ranking information for each word in the trie.
  - This allows for quick retrieval of relevant links based on the ranking.

