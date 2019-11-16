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
		if (resp["Status"] == "failed") {
			alert(resp["Message"]);
		} else {
			if (resp["Body"]["ModelIsFinished"]) {
				setTimer = null;
				window.clearInterval(setModelTimer);
				document.getElementById("modelRuntime").innerHTML = "Model Finished";
				output = processResult(resp["Body"]["Result"]);
				sessionStorage.setItem("output", JSON.stringify(output));
				console.log("OUTPUT");
				console.log(output);
				window.location.href = "/app/teams.html";
			} else {
				console.log("!! model still running");
				timer(key);
			}
		}
	});
}

function start() {
	let model_input = JSON.stringify(prepareData());

	$.ajax({
		url: "/start-model",
		type: "post",
		data: model_input,
		contentType: "application/json; charset=utf-8",
		success: function (resp) {
			console.log(resp);
			const key = resp["Key"];
			setModelTimer = setInterval(modelTimer, 1000);
			modelRuntime = 0;
			//sessionStorage.setItem("model_key", key);
			console.log("start timed checks");
			timer(key);
		}
	});
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
				console.log(resp);
				resolve(resp);
			}
		});
	});
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

	// get gender vector
	let genders = students.map(function (value, index) {
		return value[5].toLowerCase();
	});

	return ({
		num_students: num_students,
		num_teams: num_teams,
		team_size: parseInt(team_size),
		conflicts: conflicts_new,
		gpas: gpas,
		genders: genders
	});
}

function processResult(result) {

	const students = JSON.parse(sessionStorage.getItem("students"));
	const conflicts = JSON.parse(sessionStorage.getItem("conflicts"));

	console.log(result)

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
		console.log(student)
		const id = student[0];
		output["people"][id] = {
			id: id,
			firstName: student[1],
			lastName: student[2],
			email: student[3],
			gpa: student[4],
			gender: student[5],
			conflicts: []
		}
		conflicts.forEach(function (conflict) {
			if (conflict[0] == id) {
				output["people"][id]["conflicts"].push(conflict[3]);
			}
		});
	});

	return (output);
}
