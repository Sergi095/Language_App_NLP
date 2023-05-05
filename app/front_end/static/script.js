const inputLanguageSelector = document.getElementById('input-language-selector');
const outputLanguageSelector = document.getElementById('output-language-selector');

// When input language selector changes, set output language to the opposite
inputLanguageSelector.addEventListener('change', function() {
    if (inputLanguageSelector.value === 'English') {
        outputLanguageSelector.value = 'Spanish';
    } else if (inputLanguageSelector.value === 'Spanish') {
        outputLanguageSelector.value = 'English';
    }
});

// When output language selector changes, set input language to the opposite
outputLanguageSelector.addEventListener('change', function() {
    if (outputLanguageSelector.value === 'English') {
        inputLanguageSelector.value = 'Spanish';
    } else if (outputLanguageSelector.value === 'Spanish') {
        inputLanguageSelector.value = 'English';
    }
});