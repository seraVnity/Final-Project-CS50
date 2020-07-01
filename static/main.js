document.addEventListener("DOMContentLoaded", () => {
  //   const socket = io.connect(
  //     location.protocol + "//" + document.domain + ":" + location.port
  //   );
  //   // When connected, configure send
  //   socket.on("connect", () => {
  //     // Notify the server user has joined
  //     // socket.emit("game start");
  //   });
  //   socket.on("pass emojis", () => {
  //     console.log(data);
  init();

  function init() {
    openAndMatch();
  }
});

let clickedArray = [];

let count = 0;
let matched = [];

//function the rotates and matches squares on click
openAndMatch = () => {
  timer()
  const items = document.querySelectorAll(".item");
  const squares = Array.from(items);
  squares.forEach(function(square) {
    square.addEventListener("click", function() {
      // ROTATE THE SQUARE
      square.classList.add("clicked");
      square.lastElementChild.classList.remove("notmatched");
      // ADD THE CLICKED SQUARE TO THE ARRAY TO CHECK IF THEY MATCH
      if (clickedArray.length === 0) {
        console.log("first");
        clickedArray.push({ id: square.id, item: square });
      } else if (clickedArray.length === 1) {
        console.log("second");
        clickedArray.push({ id: square.id, item: square });
        checkMatch();
      } else if (clickedArray.length === 2 && !checkMatch()) {
        console.log("reset");
        reset();
        clickedArray.push({ id: square.id, item: square });
      }
    });
  });
};
checkMatch = () => {
  if (clickedArray.length === 2) {
   
    let clicked1 = clickedArray[0];
    let clicked2 = clickedArray[1];
    console.log(clicked1);
    console.log(clicked2.item.lastElementChild);
    if (clicked1.id === clicked2.id) {
      console.log("matched");
      clicked1.solved = true;
      clicked2.solved = true;
      matched.push(clicked1);
      matched.push(clicked2);
      clicked1.item.lastElementChild.classList.add("matched");
      clicked2.item.lastElementChild.classList.add("matched");

      clickedArray = [];
      return true;
    } else {
      console.log("not matched");
      clicked1.solved = false;
      clicked2.solved = false;
      clicked1.item.lastElementChild.classList.add("notmatched");
      clicked2.item.lastElementChild.classList.add("notmatched");

      return false;
    }
  }
};

reset = () => {
  clickedArray.forEach(function(element) {
    if (element.solved === false) {
      element.item.classList.remove("clicked");
      clickedArray = [];
    }
  });
};

// --------- TIMER --------------//
timer = () => {
  let timeLeft = 60;
  let setTimer = setInterval(function() {
    minutes = parseInt(timeLeft / 60, 10);
    seconds = parseInt(timeLeft % 60, 10);
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    document.querySelector(".timer").textContent = minutes + ":" + seconds;
    timeLeft -= 1;

    if (timeLeft === 0) {
      clearInterval(setTimer);
      document.querySelector(".looseOrWinBlockWindow").style.display = "block";
      document.querySelector(".looseOrWinText").innerHTML = "Loose";
    } else if (timeLeft > 0 && matched.length === 12) {
      clearInterval(setTimer);
      document.querySelector(".looseOrWinBlockWindow").style.display = "block";
      document.querySelector(".looseOrWinText").innerHTML = "Win";
    }
  }, 1000);
};

document.querySelector(".playAgain").addEventListener("click", function() {
  window.location.reload(true);
});
