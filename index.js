class Node {
    constructor(yes, no, question) {
        this.yes = yes;
        this.no = no;
        this.question = question;
    }

    setYes(yesVal){
        this.yes = yesVal;
    }

    getYes() {
        return this.yes;
    }

    setNo(noVal) {
        this.no = noVal;
    }

    getNo() {
        return this.no;
    }
}

class BinaryTree {
    constructor(node){
        this.root = node;
    }

    addNode(currentNode, newNode, side) {
        if(side == 'yes'){
            currentNode.yes = newNode;
        } else {
            currentNode.no = newNode
        }
    }

}

// Function shows intro content and hides responses
function intro() {
    console.log("Beginnning the app");
    document.getElementById("End").style.display = 'none';
    // document.getElementById("NoQuestions").style.display = 'none';
    document.getElementById("Intro").style.display = 'block';
}

function end() {
    console.log("End of app.");
    document.getElementById("Intro").style.display = 'none';
    document.getElementById("NoQuestions").style.display = 'none';
    document.getElementById("End").style.display = 'block'
}

function getButtonInput(ans) {
    var input = ans;
    console.log(ans);
    checkInput(ans);
    end();
}

function getNoQFormInput(){
    let form = document.getElementById("QInputForm");
    form.addEventListener("submit", function(event){
        event.preventDefault(); // Prevent form resubmission
        const formData = {}
        new FormData(form).forEach((value, key) => {
            formData[key] = value;
        });
        let qInput = formData.QInput;
        let yes = form.elements["parent"][0].checked; // Stores if the yes button is checked
        let no = form.elements["parent"][1].checked;  // Stores if the no button is checked
        console.log(formData);
        console.log(qInput);
        console.log(yes);
        console.log(no);
    });
}

// function checkInput(input) {
//     if (input == 'yes' && )
// }

function playAgain() {
    intro();
}

function hide(element) {
    element.style.display = 'none';
}



function main() {
    intro();
    console.log("Hello world!")

}

main();
intro();