export const validateName = (name) => {
    const regex = /^[a-zA-Z\s]*$/;
    return regex.test(name) && name.length <= 50;
};

export const validateUsername = (username) => {
    const regex = /^[a-zA-Z0-9](\w|_)*$/;
    // TODO: check db if username already exists
    return regex.test(username) && username.length <= 16;
};

export const validateEmail = (email) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email) && email.length <= 50;
};

export const validatePhoneNumber = (phoneNumber) => {
    const regex = /^(09|\+639)\d{9}$/;
    return regex.test(phoneNumber);
};

export const validatePassword = (password, newErrors) => {
    const passwordLength = password.length;
    const hasLowercase = /[a-z]/.test(password);
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialCharacter = /[!@#$%^&*()_,.?":{}|<>\-]/.test(password);

    if (passwordLength < 12 || passwordLength > 32) {
      newErrors.password = 'Password must be between 12 and 32 characters long.';
    } else if (!hasLowercase) {
      newErrors.password = 'Password must contain at least one lowercase letter.';
    } else if (!hasUppercase) {
      newErrors.password = 'Password must contain at least one uppercase letter.';
    } else if (!hasNumber) {
      newErrors.password = 'Password must contain at least one number.';
    } else if (!hasSpecialCharacter) {
      newErrors.password = 'Password must contain at least one special character.';
    }

    return newErrors;
};

export const validateLobbyCode = (lobbyCode) => {
    if (lobbyCode === '') {
        return false;
    }
    const regex = /^[a-zA-Z0-9]{6}$/;
    return regex.test(lobbyCode);
}

export const validateBotDifficulty = (diffLvl) => {
    return diffLvl >= 1 && diffLvl <= 10;
}