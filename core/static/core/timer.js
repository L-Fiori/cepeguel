const eventBox = document.getElementById("event-box")
const eventTimer = document.getElementById('event-box-timer')
const countdownBox = document.getElementById('countdown-box')
const eventDate = parseInt(eventTimer.textContent) + Date.parse(eventBox.textContent)

const myCountdown = setInterval(()=>{
    const now = new Date().getTime()
    const diff = eventDate - now

    const h = Math.floor(eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60)))
    const m = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((eventDate / (1000) - (now / (1000))) % 60)

    if (diff > 0) {
        countdownBox.innerHTML = h + " horas, " + m + " minutos e " + s + " segundos."
    } else {
        clearInterval(myCountdown)
        countdownBox.innerHTML = "Reserva expirada"
    }

}, 1000)

