from bs4 import BeautifulSoup
import re
import os
import string
from typing import List, Dict
from collections import defaultdict
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearnStopWords
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, END, Y


class TrieNode:
    def __init__(self, char: str):
        # Trie node initialization
        self.char = char
        self.parent = None
        self.children = {}
        self.isPrefix = False
        self.isIndexTerm = False
        self.counter = 1
        self.freqList = None
        self.rank = None

    def __str__(self):
        # String representation of TrieNode for debugging
        return "Node:\tchar: '{}', isPrefix: {}, isIndexTerm: {}, counter: {}, freqList: {}, rank: {}".format(
            self.char, self.isPrefix, self.isIndexTerm, self.counter, self.freqList, self.rank
        )

class Trie:
    def __init__(self):
        # Trie initialization
        self.root = TrieNode(" ")

    def addWord(self, word: str, link: str, rank: int):
        # Add word to the Trie
        node = self.root
        for char in word:
            if char in node.children:
                child = node.children[char]
                child.counter += 1
                node = child
            else:
                newNode = TrieNode(char)
                newNode.parent = node
                node.children[char] = newNode
                node = newNode

        node.isIndexTerm = True
        if node.children:
            node.isPrefix = True

        # Update rank and frequency information
        if node.rank:
            if link in node.rank and node.rank[link] != rank:
                if node.freqList and node.rank[link] in node.freqList:
                    node.freqList[rank] = node.freqList[node.rank[link]]
                    del node.freqList[node.rank[link]]
                else:
                    node.freqList = {rank: [link]}
            else:
                node.rank[link] = rank
                if node.freqList:
                    node.freqList[rank] = node.freqList.get(rank, []) + [link]
                else:
                    node.freqList = {rank: [link]}
        else:
            node.rank = {link: rank}
            if node.freqList:
                node.freqList[rank] = node.freqList.get(rank, []) + [link]
            else:
                node.freqList = {rank: [link]}

class MySearchEngine:
    def __init__(self):
        # Search Engine initialization
        self.trie = Trie()
        self.compressedTrie = Trie()

    def crawlPage(self, trie: Trie, link: str):
        # Crawl HTML page and add words to the Trie
        pageHtml = self.decodeHTMLFile(link)
        parsedHTML = BeautifulSoup(pageHtml, 'html.parser')
        HTMLToText = parsedHTML.get_text()
        htmlWords = self.parseText(HTMLToText)
        htmlRank = self.findRank(htmlWords)
        for word, rank in htmlRank.items():
            trie.addWord(word, link, rank)

    def compressTrie(self):
        # Compress Trie by merging nodes with a single child
        def helperFunctionCT(node):
            children = list(node.children.values())
            if not node.isPrefix and len(children) == 1:
                child = children[0]
                child.parent = None
                
                del node.parent.children[node.char]
                
                node.char += child.char
                node.parent.children[node.char] = node
                node.children = child.children
                node.isPrefix = child.isPrefix
                node.isIndexTerm = child.isIndexTerm
                node.freqList = child.freqList
                node.rank = child.rank
                helperFunctionCT(node)
            
            elif len(children) > 1:
                for child in children:
                    helperFunctionCT(child)

        for child in list(self.compressedTrie.root.children.values()):
            helperFunctionCT(child)

    def searchWord(self, word: str) -> Dict[int, List[str]]:
        # Search for a word in the compressed Trie
        root = self.compressedTrie.root

        def helperFunctionSW(node: TrieNode, string: str) -> Dict[int, List[str]]:
            for char, child in node.children.items():
                if char == string and child.isIndexTerm:
                    return child.freqList
                elif string.startswith(char):
                    return helperFunctionSW(child, string[len(char):])
            return {}

        return helperFunctionSW(root, word)

    def decodeHTMLFile(self, link: str) -> str:
        # Read and decode HTML file
        path = f"/Users/jigglypuff/Documents/Deepali Nagwade - Final Project/HTML Files/{link}"
        with open(path, 'rb') as file:
            return file.read().decode('utf-8', errors='ignore')


    @staticmethod
    def parseText(text: str) -> List[str]:
        # Parse text and remove stop words
        stopWords = set(sklearnStopWords)
        words = re.sub(r"[^\w]", " ", text.lower()).split()
        return [word for word in words if word not in stopWords]

    @staticmethod
    def findRank(listOfWords: List[str]) -> Dict[str, int]:
        # Find rank of words in a list
        rankDictionary = defaultdict(int)
        for word in listOfWords:
            rankDictionary[word] += 1
        return dict(rankDictionary)


class SearchApp:
    def __init__(self, master):
        # GUI for the Search Engine
        self.master = master
        self.master.title("Search Engine - Deep's Version")

        # Entry for user input
        self.search_text = Entry(master)
        self.search_text.pack(pady=10)

        # Button to trigger search
        self.searchButton = Button(master, text="Search", command=self.search)
        self.searchButton.pack()
        
        # Button to quit the application
        self.quitButton = Button(master, text="Quit", command=self.quit_app)
        self.quitButton.pack()

        # Text box to display results
        self.resultText = Text(master, height=10, width=50, wrap=tk.WORD)
        self.resultText.pack()

        # Scrollbar for the resultText
        self.scrollbar = Scrollbar(master, command=self.resultText.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=Y)
        self.resultText.config(yscrollcommand=self.scrollbar.set)

        

    def search(self):
        # Trigger search when the search button is pressed
        query = self.search_text.get().lower()
        translation = str.maketrans("", "", string.punctuation)
        query = query.translate(translation)

        if query == "quit":
            self.quit_app()

        searchData = searchEngineObject.searchWord(query)
        self.display_results(searchData)

    def display_results(self, search_results):
        # Display search results in the resultText box
        self.resultText.delete(1.0, END)

        if search_results:
            sorted_result_data = sorted(list(search_results.items()), key=lambda entry: entry[0], reverse=True)
            for entry in sorted_result_data:
                for result in entry[1]:
                    self.resultText.insert(END, f"{result}\n")
            self.resultText.insert(END, "\n")
        else:
            self.resultText.insert(END, "Not Found!\n")

    def quit_app(self):
        # Quit the application
        self.master.destroy()


if __name__ == "__main__":
    # Main application logic
    htmlDirectory = "/Users/jigglypuff/Documents/Deepali Nagwade - Final Project/HTML Files"
    htmlFiles = []

    for f in os.listdir(htmlDirectory):
        fullPath = os.path.join(htmlDirectory, f)
        if os.path.isfile(fullPath):
            htmlFiles.append(f)

    searchEngineObject = MySearchEngine()

    for htmlFile in htmlFiles:
        searchEngineObject.crawlPage(searchEngineObject.compressedTrie, htmlFile)

    searchEngineObject.compressTrie()

    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
