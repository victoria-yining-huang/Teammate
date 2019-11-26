// Script file for HTML page: generate_teams.html

var setModelTimer;
var modelRuntime = 0;

function modelTimer() {
	modelRuntime = modelRuntime + 1;
	document.getElementById("modelRuntime").innerHTML =
		String(modelRuntime) + " seconds";
}


window.onload = function startModel() {
	this.start()
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function timer(key) {
	await sleep(1000);
	check(key).then(function (resp) {
		if (resp["ModelIsFinished"]) {
			setTimer = null;
			window.clearInterval(setModelTimer);
			document.getElementById("modelRuntime").innerHTML = "Model Finished";
			output = processResult(resp["Result"]);
			if (output["error"] == null) {
				sessionStorage.setItem("output", JSON.stringify(output));
				window.location.href = "/app/teams.html";
			} else {
				handleError(output)
			}
		} else {
			timer(key);
		}
	});
}

function start() {
	const prep_data = prepareData();
	if (prep_data["error"] == null) {
		let model_input = JSON.stringify(prep_data);
		$.ajax({
			url: "/start-model",
			type: "post",
			data: model_input,
			contentType: "application/json; charset=utf-8",
			success: function (resp) {
				const key = resp["Key"];
				setModelTimer = setInterval(modelTimer, 1000);
				modelRuntime = 0;
				timer(key);
			},
			error: function (resp) {
				handleError(resp)
			}
		});
	} else {
		handleError(prep_data)
	}
}

function check(key) {
	return new Promise(function (resolve) {
		$.ajax({
			url: "/status",
			type: "post",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				key: key
			}),
			success: function (resp) {
				resolve(resp);
			},
			error: function (resp) {
				handleError({
					error: true,
					message: "An internal error occured while running the model. Please restart."
				})
			}
		});
	});
}

function handleError(resp) {
	console.log(resp)
	document.getElementById("loader").classList.add("hidden");
	document.getElementById("error").classList.remove("hidden");
	document.getElementById("error-message").innerHTML = resp["message"];
}

function ping() {
	$.ajax({
		url: "/ping",
		type: "get",
		success: function (resp) {
			console.log(resp);
		}
	});
}

function prepareData() {
	const students = JSON.parse(sessionStorage.getItem("students"));
	const conflicts = JSON.parse(sessionStorage.getItem("conflicts"));
	const team_size = sessionStorage.getItem("team_size");
	const ifgpa = sessionStorage.getItem("ifgpa");

	if (students != null && conflicts != null && team_size != null) {

		try {

			let num_students = students.length;
			let num_teams =
				Math.floor(num_students / team_size) +
				Math.min(1, num_students % team_size);

			// get ids vector
			const ids = students.map(function (value, index) {
				return value[0];
			});

			// deduplicate conflicts
			var conflicts_new = [];
			for (var i = 0; i < conflicts.length; i++) {
				const person_a = ids.indexOf(conflicts[i][0]);
				const person_b = ids.indexOf(conflicts[i][3]);
				const conflict = [person_a, person_b];
				const conflict_inverse = [person_b, person_a]
				if (!conflicts_new.includes(conflict_inverse)) {
					conflicts_new.push(conflict)
				}
			}

			// get gpa vector
		
			let gpas = students.map(function (value, index) {
				return parseInt(value[4]);
			});

			return ({
				num_students: num_students,
				num_teams: num_teams,
				team_size: parseInt(team_size),
				conflicts: conflicts_new,
				gpas: gpas,
				ifgpa : ifgpa
			});

		} catch (error) {
			return {
				error: true,
				message: "An error occured while processing the input data.\n\nError Details:\n" + error
			};
		}
	}
	else {
		return {
			error: true,
			message: "The input data is missing. Please restart the team process."
		};
	}
}

function processResult(result) {

	try {

		const students = JSON.parse(sessionStorage.getItem("students"));
		const conflicts = JSON.parse(sessionStorage.getItem("conflicts"));

		var output = {
			model: {
				hasConflicts: result["hasConflicts"]
			},
			teams: {},
			people: {}
		}

		// Place students in teams
		for (var i = 0; i < result["assignments"].length; i++) {
			team = result["assignments"][i] + 1;
			student = students[i][0]
			if (team in output["teams"]) {
				output["teams"][team]["members"].push(student)
			} else {
				output["teams"][team] = {}
				output["teams"][team]["members"] = [student]
			}
		}

		// Create students
		students.forEach(function (student) {
			const id = student[0];
			output["people"][id] = {
				id: id,
				firstName: student[1],
				lastName: student[2],
				email: student[3],
				gpa: parseInt(student[4]), //fixes the formatting error
				conflicts: []
			}
			conflicts.forEach(function (conflict) {
				if (conflict[0] == id) {
					output["people"][id]["conflicts"].push(conflict[3]);
				}
			});
		});

		return (output);

	} catch (error) {
		return {
			error: true,
			message: "An error occured while processing the model output.\n\nError Details:\n" + error
		};
	}
}

function restartApp() {
	sessionStorage.clear()
	window.location.href = "/app/setup.html"
}