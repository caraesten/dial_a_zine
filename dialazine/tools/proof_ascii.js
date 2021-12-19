class AsciiScanner {
    static ASCII_REGEX = /([\u{0080}-\u{FFFF}]+)/gu;
    constructor(inputElement, matchesOutput, textOutput) {
        this.inputElement = inputElement;
        this.matchesOutput = matchesOutput;
        this.textOutput = textOutput;
    }

    start() {
        this.inputElement.addEventListener('input', (event) => {
            const text = event.target.value;
            this.onTextChange(text);
        })
    }

    onTextChange(newText) {
        const output = newText.replace(AsciiScanner.ASCII_REGEX, (match) => {
            return `<span class='invalid'>${match}</span>`;
        });
        this.textOutput.innerHTML = output;

        const errors = ((newText || '').match(AsciiScanner.ASCII_REGEX) || []).length;
        this.matchesOutput.innerHTML = `Found: ${errors} non-ASCII blocks`
    }
}

window.onload = function() {
    const scanner = new AsciiScanner(
        document.getElementById('text-input'),
        document.getElementById('matches-output'),
        document.getElementById('text-output'));
    
    scanner.start();
}
