const StartModeElement = document.getElementById("start-mode");
const DiffLockElement = document.getElementById("diff-lock");

const HeadingElement = document.getElementById("heading");
const SpeedElement = document.getElementById("speed");

const TimeDeltaElement = document.getElementById("delta");
const TimePreviousElement = document.getElementById("previous");
const TimeElapsedElement = document.getElementById("elapsed");

const FuelGaugeElement = document.getElementById("fuel-gauge");
// const FuelTextElement = document.getElementById("fuel-text-container");
const FuelPercentElement = document.getElementById("fuel-percent");
const FuelVolumeElement = document.getElementById("fuel-volume");

const RealDateElement = document.getElementById("real-date");
const RealTimeElement = document.getElementById("real-time");

let dateObj = null;
let apiData = null;

function replaceText(element, text) {
  if (element) {
    element.innerText = text;
  }
}

function setIndicatorState(element, state) {
  if (element) {
    element.style.color = state ? 'white' : 'gray'
  }
}

function setField(selector, value) {
  switch (selector) {
    case 'fuel-percent':
      replaceText(FuelPercentElement, `${value}%`);
      FuelGaugeElement.style.height = `${value}%`;
      FuelGaugeElement.style.backgroundColor = `hsl(${1.2 * parseInt(value)}, 80%, 50%)`
      // FuelTextElement.style.color = `hsl(${1.2 * parseInt(value) + 270}, 80%, 50%)`
      break;

    case 'fuel-volume':
      replaceText(FuelVolumeElement, `${value}mL`);
      break;

    case 'speed':
      replaceText(SpeedElement, `${value}kts`);
      break;

    case 'heading':
      replaceText(HeadingElement, value.toString().padStart(3, '0'));
      break;

    case 'start-mode':
      setIndicatorState(StartModeElement, !!value);
      break;

    case 'diff-lock':
      setIndicatorState(DiffLockElement, !!value);
      break;

    default:
      break;
  }
}

async function run_update() {
  dateObj = new Date();
  replaceText(RealTimeElement, dateObj.toTimeString().split(' ')[0]);

  try {
    apiData = await (await fetch('/api/v1/systems/all')).json()
  } catch (error) {

  }

  if (apiData) {
    setField('fuel-percent', apiData.fuel.level);
    setField('fuel-volume', apiData.fuel.volume);

    setField('speed', apiData.gps.speed);
    setField('heading', apiData.gps.heading);

    setField('start-mode', apiData.other.start_mode);
    setField('diff-lock', apiData.other.diff_lock);
  }
  console.log(`Update Time: ${new Date() - dateObj}ms`)
}

window.addEventListener('DOMContentLoaded', () => {
  replaceText(RealDateElement, new Date().toLocaleDateString());

  fetch('/api/v1/status').then(res => {
    if (JSON.parse(res).mode == 'test') {
      document.getElementById('test-mode').style.color = 'white';
    }
  })
  
  setInterval(run_update, 1000 / 10);

});
