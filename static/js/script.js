   function copyText(text) {

        // Create a temporary textarea element

        const textarea = document.createElement('textarea');

        textarea.value = text; // Set the value to the text you want to copy

        document.body.appendChild(textarea); // Append it to the body

        textarea.select(); // Select the text

        document.execCommand('copy'); // Copy the text to the clipboard

        document.body.removeChild(textarea); // Remove the textarea

        alert('Copied: ' + text); // Optional: Alert the user

    }