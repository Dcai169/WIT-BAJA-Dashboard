// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
// import got from 'got';

function replaceText(selector: string, text: string): void {
  const element = document.getElementById(selector);
  if (element) {
    element.innerText = text;
  }
}

function setIndicatorState(selector: string, state: boolean): void {
  const element = document.getElementById(selector);
  if (element) {
    element.style.color = state ? 'white' : 'gray'
  }
}

function setField(selector: string, value: string): void {
  switch (selector) {
    case 'fuel-percent':
      replaceText("fuel-percent", `${value}%`);
      let gaugeDOMObject = document.getElementById("fuel-gauge");
      gaugeDOMObject.style.height = `${value}%`;
      gaugeDOMObject.style.backgroundColor = `hsl(${1.2*parseInt(value)}, 80%, 50%)`
      break;

    case 'fuel-estimate':
      replaceText("fuel-estimate", `${value}min`);
      break;

    case 'speed':
      replaceText("speed", `${value}mph`);
      break;

    case 'heading':
      replaceText("heading", value.toString().padStart(3, '0'));
      break;

    // case 'real-date':
    //   replaceText("real-date", new Date().toDateString());
    //   break;

    // case 'real-time':
    //   replaceText("real-time", new Date().toTimeString().split(' ')[0]);
    //   break;

    case 'start-mode':
      setIndicatorState("start-mode", !!value);
      break;

    case 'diff-lock':
      setIndicatorState("diff-lock", !!value);
      break;
  
    default:
      replaceText(selector, value);
      break;
  }
}

function update(): void {
  replaceText("real-time", new Date().toTimeString().split(' ')[0]);

  // Get data
  // got({url: 'https://localhost/api/v1/system_status'})
  //   .then(response => {
  //     const data = JSON.parse(response.body);
  //     // Update fields
  //     Object.entries(data).forEach( entry => {
  //       setField(...( entry as [string, string] ));
  //     });
  //   });
}

window.addEventListener("DOMContentLoaded", () => {
  replaceText("real-date", new Date().toDateString());
  setInterval(update, 100)
});
