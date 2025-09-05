let cronometro = 0;
let bruto = 0;
let rodando = false;
let intervaloLiquido;
let intervaloBruto;

const cronometroDiv = document.getElementById('cronometro');
const tempoBrutoDiv = document.getElementById('tempo-bruto');
const iniciarBtn = document.getElementById('iniciar');
const reiniciarBtn = document.getElementById('reiniciar');

iniciarBtn.onclick = () => {
    if (!rodando) {
        rodando = true;
        iniciarBtn.innerText = "Pausar";
        iniciarBtn.style.background = "orange";
        iniciarBtn.style.color = "#333";

        intervaloLiquido = setInterval(() => {
            cronometro++;
            cronometroDiv.innerText = formatar(cronometro);
            document.getElementById('tempo_liquido').value = formatar(cronometro);
        }, 1000);

        if (!intervaloBruto) {
            intervaloBruto = setInterval(() => {
                bruto++;
                tempoBrutoDiv.innerText = "Tempo Bruto: " + formatar(bruto);
                document.getElementById('tempo_bruto').value = formatar(bruto);
            }, 1000);
        }
    } else {
        rodando = false;
        iniciarBtn.innerText = "Continuar";
        iniciarBtn.style.background = "green";
        iniciarBtn.style.color = "#fff";
        clearInterval(intervaloLiquido);
    }
};

reiniciarBtn.onclick = () => {
    if (confirm("Tem certeza que quer reiniciar o cronômetro?")) {
        rodando = false;
        clearInterval(intervaloLiquido);
        clearInterval(intervaloBruto);
        intervaloBruto = null;
        cronometro = 0;
        bruto = 0;
        cronometroDiv.innerText = "00:00:00";
        tempoBrutoDiv.innerText = "Tempo Bruto: 00:00:00";
        iniciarBtn.innerText = "Iniciar";
        iniciarBtn.style.background = "green";
        iniciarBtn.style.color = "#fff";
    }
};

function confirmarFinalizacao() {
    return confirm("Finalizar sessão?") && confirm("Salvar sessão?");
}

function formatar(segundos) {
    const h = String(Math.floor(segundos / 3600)).padStart(2, '0');
    const m = String(Math.floor((segundos % 3600) / 60)).padStart(2, '0');
    const s = String(segundos % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
}
