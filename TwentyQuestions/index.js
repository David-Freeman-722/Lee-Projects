class Node {
    constructor(question, parent = null, yes = null, no = null) {
        this.question = question;
        this.parent = parent;
        this.yes = yes;
        this.no = no;
    }
    setParent(node){
        this.parent = node;
    }
    getParent() {
        return this.parent;
    }
    setQuestion(question) {
        this.question = question;
    }
    getQuestion() {
        return this.question;
    }
    setYes(node){
        this.yes = node;
        if(node){
            node.parent = this;
        }
    }
    getYes() {
        return this.yes;
    }
    setNo(node) {
        this.no = node;
        if(node){
            node.parent = this;
        }
    }
    getNo() {
        return this.no;
    }
}

class BinaryTree {
    constructor(){
        this.root = null;
        this.size = 0;
    }

    addNode(question, side) {
        if(!this.root){
            this.root = new Node(question);
            return;
        }
        var newNode = new Node(question);
        if(side == "yes"){
            currentNode.setYes(newNode);
        } else {
            currentNode.setNo(newNode);
        }
        newNode.setParent(currentNode);
        this.size += 1;
    }

    getRoot(){
        return this.root;
    }

    getSize(){
        return this.size;
    }
}


// Creates a JSON file out of the current tree
function treeToJSON(node){
    if(!node) return null;
    return {
        question: node.question,
        yes: treeToJSON(node.yes),
        no: treeToJSON(node.no),
    };
}

function jsonToTree(json) {
    if (!json) return null; // Base case for null nodes
    const node = new Node(json.question);
    node.yes = jsonToTree(json.yes);
    node.no = jsonToTree(json.no);
    return node;
}
  
function loadTreeFromJSON(file, callback) {
    const reader = new FileReader();
    reader.onload = function (event) {
      try {
        const jsonData = JSON.parse(event.target.result);
        const jsonTree = new BinaryTree();
        jsonTree.root = jsonToTree(jsonData);
        callback(jsonTree); // Call the provided function with the reconstructed tree
      } catch (error) {
        console.error("Error parsing JSON:", error);
      }
    };
    reader.readAsText(file);
}
  

function downloadJSON(tree, filename = "binary_tree.json") {
    const jsonString = JSON.stringify(treeToJSON(tree.root), null, 2); // Pretty print
    const blob = new Blob([jsonString], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Function shows intro content and hides responses
function intro() {
    console.log("Beginnning the app");
    document.getElementById("End").style.display = 'none';
    document.getElementById("NoQuestions").style.display = 'none';
    document.getElementById("Intro").style.display = 'block';
    document.getElementById("introQ").textContent = currentNode.getQuestion();
}

// Shows screen asking user to provide a question
function noQuestions() {
    console.log("No more questions");
    document.getElementById("Intro").style.display = 'none';
    document.getElementById("End").style.display = 'none';
    document.getElementById("NoQuestions").style.display = 'block';
}

// Shows end screen content and offers for the user to play again
function end() {
    console.log("End of app.");
    document.getElementById("Intro").style.display = 'none';
    document.getElementById("NoQuestions").style.display = 'none';
    document.getElementById("End").style.display = 'block'
    document.getElementById("answer").textContent = currentNode.getQuestion();
    currentNode = tree.getRoot();
    document.getElementById("json").value = null;
}

function getNoQFormInput(form){
    let qInput = form.elements["QInput"].value;
    let yesGuess = form.elements["yesGuess"].value;
    document.getElementById("QInput").value = ""; // Resets input text box
    document.getElementById("yesGuess").value = ""; // Resets guess text box
    let oldGuess = currentNode.getQuestion();
    currentNode.setQuestion(qInput); // Replaces bad node question with better question
    tree.addNode(oldGuess, "no"); // Adds old guess as no child of new question
    tree.addNode(yesGuess, "yes"); // Adds new yes guess as yes child of new question
    downloadJSON(tree);
}

function treeLogic(ans){
    var root = tree.getRoot();
    console.log("START OF TREE LOGIC")
    console.log("Tree logic root " + currentNode.getQuestion());
    console.log("Tree logic child yes " + currentNode.getYes());
    console.log("Tree logic child no " + currentNode.getNo())
    if(ans){
        if(currentNode.getYes() == null){ // If the yes node has no children end it
            end();
        } else { // Go to more questions 
            currentNode = currentNode.getYes();
            intro();
        }
    } else {
        if(currentNode.getNo() == null){ // If the yes node has no children end it
            noQuestions(); // Creates a new root node every single time
        } else { // Go to more questions 
            currentNode = currentNode.getNo();
            intro();
        }
    }
}



// Defines on event functions that fire when certain events occur.  Used to get
// js out of the htm file.

// Event listeners for yes and no buttons on the intro page
const introYesButton = document.getElementById("inYes");
const introNoButton  = document.getElementById("inNo");

// Yes button listener switches the page to end div
introYesButton.addEventListener("click", () => {
    treeLogic(true);
  });


// No button listener switches the page to end screen. Switches back to intro with 
introNoButton.addEventListener("click", () => {
    treeLogic(false);
});

// Event listener for play again button to move back to intro screen
const playAgainButton = document.getElementById("playAgain");
playAgainButton.addEventListener("click", () => {
    intro();
});

const inputFormSubmit = document.getElementById("QInputForm");
inputFormSubmit.addEventListener("submit", function(event) {
    event.preventDefault();
    getNoQFormInput(inputFormSubmit);
    currentNode = tree.getRoot();
    intro();
});

// Retrieves tree from JSON file
document.getElementById("json").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        loadTreeFromJSON(file, (jsonTree) => {
          tree = jsonTree;
          currentNode = tree.getRoot();
          intro();
        });
    } else {
        currentNode = tree.getRoot();
        intro();
    }
})

document.addEventListener("DOMContentLoaded", function(){
    intro();
})

// Global vars for program to run
var tree = null;
var firstQuestion = "Are you thinking of a parrot?";
tree = new BinaryTree();
tree.addNode(firstQuestion);
var currentNode = tree.getRoot();


