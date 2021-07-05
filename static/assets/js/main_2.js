console.log('hello world')

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class= "h5 mb-3"> Êtes-vous sûr de vouloir commencer "<b> ${name} </b>" ?</div>
        <div class="text-muted">
        <ul>
            <li> difficulty : <b> ${difficulty} </b></li>
            <li> number de questions : <b> ${numQuestions} </b></li>
            <li> score pour passer  : <b> ${scoreToPass} %</b></li>
            <li> temps pour passer  : <b> ${time} min</b></li>
        </ul>
    
    `
    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk 
    })

}))