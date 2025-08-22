const carCanvas = document.getElementById("carCanvas");
carCanvas.width = 200;
const networkCanvas = document.getElementById("nnCanvas");
networkCanvas.width = 300;

const carContext = carCanvas.getContext("2d");
const networkContext = networkCanvas.getContext("2d");
const road = new Road(carCanvas.width / 2, carCanvas.width * 0.9);
const N = 100;
const cars = generateCars(N);
const traffic = [
  new Car(road.getLaneCenter(1), -150, 30, 50, "DUMMY", 2),
  new Car(road.getLaneCenter(0), -300, 30, 50, "DUMMY", 2),
  new Car(road.getLaneCenter(2), -300, 30, 50, "DUMMY", 2),
  new Car(road.getLaneCenter(0), -500, 30, 50, "DUMMY", 2),
    new Car(road.getLaneCenter(1), -500, 30, 50, "DUMMY", 2),
   
    new Car(road.getLaneCenter(0), -800, 30, 50, "DUMMY", 2),
    new Car(road.getLaneCenter(1), -800, 30, 50, "DUMMY", 2),
];
let bestCar = cars[0];
if (localStorage.getItem("bestBrain")) {
  for (let i = 0; i < cars.length; i++) {
    cars[i].brain = JSON.parse(localStorage.getItem("bestBrain"));
    if (i != 0) {
      NeuralNetwork.mutate(cars[i].brain, 0.2);
    }
  }
}

animate();

function save() {
  localStorage.setItem("bestBrain", JSON.stringify(bestCar.brain));
}

function discard() {
  localStorage.removeItem("bestBrain");
}

function generateCars(N) {
  const cars = [];
  for (let i = 1; i <= N; i++) {
    cars.push(new Car(road.getLaneCenter(1), 100, 30, 50, "AI"));
  }
  return cars;
}

function animate() {
  for (let i = 0; i < traffic.length; i++) {
    traffic[i].update(road.borders, []);
  }
  for (let i = 0; i < cars.length; i++) {
    cars[i].update(road.borders, traffic);
  }

  carCanvas.height = window.innerHeight;
  networkCanvas.height = window.innerHeight;

  // ✅ safer best car selection
  bestCar = cars.find((car) => car.y == Math.min(...cars.map((car) => car.y)));

  carContext.save();
  carContext.translate(0, -bestCar.y + carCanvas.height * 0.7);

  road.draw(carContext);

  for (let i = 0; i < traffic.length; i++) {
    traffic[i].draw(carContext, "red");
  }

  carContext.globalAlpha = 0.2;
  for (let i = 0; i < cars.length; i++) {
    cars[i].draw(carContext, "blue");
  }
  carContext.globalAlpha = 1;

  bestCar.draw(carContext, "blue", true);

  carContext.restore();

  // 🧠 optional: show NN of best car
  // Visualizer.drawNetwork(networkContext, bestCar.brain);

  requestAnimationFrame(animate);
}
