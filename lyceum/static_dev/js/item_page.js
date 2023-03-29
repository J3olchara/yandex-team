const value = document.querySelector(".range_label")
const input = document.querySelector(".form-range")
value.textContent = input.value
input.addEventListener("input", (event) => {
  value.textContent = event.target.value
})