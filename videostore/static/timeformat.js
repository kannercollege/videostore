var items = document.querySelectorAll(".unixtime");

for (let i = 0; i < items.length; i++) {
  const element = items[i];
  const date = new Date(parseInt(element.innerHTML) * 1000);

  element.innerHTML = `${date.toLocaleDateString()} at ${date.toLocaleTimeString()}`;
}
