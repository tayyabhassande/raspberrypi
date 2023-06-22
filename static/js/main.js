/**
 * Updates the current digit, distance and motor status calling
 * the corresponding methods.
 */
function updateStatus() {
    // Update current digit based on Open CV

    (async () => await updateCurrentDigitOpenCV())();
    // Update motor status
    //...
    (async () => await updateMotorStatus())();

    // Update current digit based on OpenCV
    //...
   
    (async () => await updateCurrentShapeDistance())();
   
    // Update current distance
    //...
    (async () => await updateDistance())();

}

/**
 * Update the current digit based on OpenCV.
 */
async function updateCurrentDigitOpenCV() {
    try {
        // Request digit from server
        const requestResult = await requestDigitFromOpenCV()
        // Get the HTML element where the status is displayed
        const eight_open_cv = document.getElementById('eight_open_cv')
        eight_open_cv.innerHTML = requestResult.data[0]
        const three_open_cv = document.getElementById('three_open_cv')
        three_open_cv.innerHTML = requestResult.data[1]
        const one_open_cv = document.getElementById('one_open_cv')
        one_open_cv.innerHTML = requestResult.data[2]

    } catch (e) {
        console.log('Error getting the digit based on OpenCV', e)
        updateStatus('Error getting the digit based on OpenCV')
    }
}

/**
 * Function to request the server to update the current
 * digit based on OpenCV.
 */
function requestDigitFromOpenCV() {
    try {
        // Make request to server
        return axios.get('/get_digit_from_opencv')
    } catch (e) {
        console.log('Error getting the status', e)
        updateStatus('Error getting the status')

    }
}


/**
 * Function to request the server to start the motor.
 */
function requestStartMotor() {
    //...
    axios.get('/start_motor')
}


/**
 * Function to request the server to stop the motor.
 */
function requestStopMotor() {
    //...
    axios.get('/stop_motor')
}

/**
 * Update the status of the motor.
 * @param {String} status
 */

/**
 * Update the status of the motor.
 * @param {String} status
 */
async function updateMotorStatus() {
    try {
        // Request distance from server
        const statusResult = await requestMotorStatus()
        const m_status = document.getElementById('motor_status')
        m_status.innerHTML = statusResult.data


    } catch (e) {
        console.log('Error getting the Motor Status', e)
        updateStatus('Error getting the Motor Status')
    }
}

async function requestMotorStatus() {
    //...
     try {
        // Make request to server
        return axios.get('/motor_status')
    } catch (e) {
        console.log('Error getting the distance', e)
        updateStatus('Error getting the distance')

    }
}


/**
 * Update the current digit based on distance sensor.
 */
async function updateDistance() {
    // Get the HTML element where the status is displayed
    // ...
    try {
        // Request distance from server
        const requestResult = await requestDistance()
        const distance = document.getElementById('distance')
        distance.innerHTML = requestResult.data

    } catch (e) {
        console.log('Error getting the shape based on Distance', e)
        updateStatus('Error getting the shape based on Distance')
    }

}


/**
 * Function to request the server to get the distance from
 * the rod to the ultrasonic sensor.
 */
function requestDistance() {
    //...
    try {
        // Make request to server
        return axios.get('/get_distance')
    } catch (e) {
        console.log('Error getting the distance', e)
        updateStatus('Error getting the distance')

    }
}



/**
 * Update the current digit based on distance sensor.
 */
async function updateCurrentDigitDistance() {
    // Get the HTML element where the status is displayed
    // ...
    try {
        // Request shape from server
        const requestResult = await requestDigitFromOpenCV()
        // Get the HTML element where the status is displayed
        const eight_distance = document.getElementById('8_distance')
        eight_distance.innerHTML = requestResult.data[0]
        const three_distance = document.getElementById('3_distance')
        three_distance.innerHTML = requestResult.data[1]
        const one_distance = document.getElementById('1_distance')
        one_distance.innerHTML = requestResult.data[2]

    } catch (e) {
        console.log('Error getting the shape based on Distance', e)
        updateStatus('Error getting the shape based on Distance')
    }
}


/**
 * Function to request the server to get the digit based
 * on distance only.
 */
function requestDigitFromDistance() {
    //...
    try {
        // Make request to server
        return  axios.get('/get_shape_from_distance')
    } catch (e) {
        console.log('Error getting the shape', e)
        updateStatus('Error getting the shape')

    }

}
