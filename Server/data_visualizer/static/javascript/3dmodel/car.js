let camera, scene, renderer;
//let stats;
let grid;
let controls;
const wheels = [];
const materials ={};
let latestUpdate = {};
var carModel = undefined;
var raycaster = new THREE.Raycaster();
var mousePointer = new THREE.Vector2();
function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}
function loadDataOnInterval(){
	sensors = ["front_left_wheel_pressure","front_right_wheel_pressure","rear_left_wheel_pressure","rear_right_wheel_pressure"];
	$.ajax({
		'url': '/rest_api/LatestValues',
		'type': 'GET',
		'data': {
			sensor: sensors,
		},
		'success': function (data) {
			latestUpdate = data;
			for (const [key, value] of Object.entries(data)) {
				//Y : 2.6 = X : 0.08 
				let r = 0.08-(parseFloat(value.data)*0.08)/2.6;
				splitted = key.split("_");
				carModel.getObjectByName(`${splitted[0]}_${splitted[1]}_tire`).material.color.setRGB(r,0,0);
			}
		},
		'error': function (request, error) {
			console.log("Error reading data");
		}
	});
}
function onMouseClicked(event){
	//mousePointer.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	//mousePointer.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	var rect = renderer.domElement.getBoundingClientRect();
	mousePointer.x = ( ( event.clientX - rect.left ) / ( rect.width - rect.left ) ) * 2 - 1;
	mousePointer.y = - ( ( event.clientY - rect.top ) / ( rect.bottom - rect.top) ) * 2 + 1;
	raycaster.setFromCamera(mousePointer, camera);
	// let h = new THREE.ArrowHelper(raycaster.ray.direction, raycaster.ray.origin, 300, 0xff0000);
	// scene.add(h);
	const intersects = raycaster.intersectObjects(scene.children);
	for ( let i = 0; i < intersects.length; i ++ ) {
		let match = intersects[i].object.name.match(/(front|rear)_(left|right)_(brake|rim|tire|disc)/);
		if(match != null){
			new_sensor_name = `${match[1]}_${match[2]}_wheel_pressure` 
			if(new_sensor_name === wheel_sensor) break;
			wheel_sensor = new_sensor_name;
			title = capitalizeFirstLetter(wheel_sensor);
			title = title.split("_").join(" ");
			wheelChart.destroy();
			wheelConfig.options.plugins.title.text = title;
			wheelChart = new Chart($("#wheel-chart"), wheelConfig);
			loadWheelData(wheelChart, true);
			break;
		}
		else if(intersects[i].object.name === "chassis"){
			break;
		}
	}
}
var SpeedRpmChart = null;
var wheelChart = null;
function init() {

	SpeedRpmChart = new Chart($("#SpeedRpmChart"), SpeedRpmConfig);
    loadData(SpeedRpmChart);
	wheelChart = new Chart($("#wheel-chart"), wheelConfig);
    loadWheelData(wheelChart, true);
	//Boilerplate code to render the scene
	const container = document.getElementById( 'container' );
	container.addEventListener('click',onMouseClicked)
	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.setAnimationLoop( render );
	renderer.outputEncoding = THREE.sRGBEncoding;
	renderer.toneMapping = THREE.ACESFilmicToneMapping;
	renderer.toneMappingExposure = 0.85;
	container.appendChild( renderer.domElement );
	window.addEventListener( 'resize', onWindowResize );
	//stats = new Stats();
	//container.appendChild( stats.dom );
	//Adding camera
	camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 0.1, 100 );
    camera.position.set( 0, 4,10);

    //Adding orbital control to navigate the scene. controls.reset to reset camera to this position
	controls = new THREE.OrbitControls( camera, container );
	controls.enableDamping = true;
	controls.maxDistance = 9;
	controls.target.set( 0, 0.5, 0 );
	controls.update();

	//Create a scene with a grid
	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0x333333 );
	scene.environment = new THREE.RGBELoader().load(texture);
	scene.environment.mapping = THREE.EquirectangularReflectionMapping;
    //scene.fog = new THREE.Fog( 0x333333, 10, 15 );
	grid = new THREE.GridHelper( 100, 100, 0xffffff, 0xffffff );
	grid.material.opacity = 0.2;
	grid.material.depthWrite = false;
	grid.material.transparent = true;
	//const light = new THREE.AmbientLight( 0x404040,10 ); // soft white light
    //scene.add( light );
    const spotLight = new THREE.SpotLight( 0xffffff,3 );
    spotLight.position.set( 2, 100, 0 );
    scene.add( spotLight );

    //const spotLightHelper = new THREE.SpotLightHelper( spotLight );
    //scene.add( spotLightHelper );
    
    scene.add( grid );

	// Car
	const dracoLoader = new THREE.DRACOLoader();
	dracoLoader.setDecoderPath( 'js/libs/draco/gltf/' );
	const loader = new THREE.GLTFLoader();
	loader.setDRACOLoader( dracoLoader );
	loader.load(car_gltf, function ( gltf ) {
		
		carModel = gltf.scene;
        wheels.push(carModel.getObjectByName('rear_left_rim'))
        wheels.push(carModel.getObjectByName('rear_right_rim'))
        wheels.push(carModel.getObjectByName('front_left_rim'))
        wheels.push(carModel.getObjectByName('front_right_rim'))
		carModel.getObjectByName('rear_left_tire').material = carModel.getObjectByName('rear_left_tire').material.clone();
		carModel.getObjectByName('rear_right_tire').material = carModel.getObjectByName('rear_right_tire').material.clone();
		carModel.getObjectByName('front_left_tire').material = carModel.getObjectByName('front_left_tire').material.clone();
		carModel.getObjectByName('front_right_tire').material = carModel.getObjectByName('front_right_tire').material.clone();
		materials["rear_left_tire"] = carModel.getObjectByName('rear_left_tire').material
		materials["rear_right_tire"] = carModel.getObjectByName('rear_right_tire').material
		materials["front_left_tire"] = carModel.getObjectByName('front_left_tire').material
		materials["front_right_tire"] = carModel.getObjectByName('front_right_tire').material
        scene.add(carModel)
	} );
	setInterval(() => {
		//loadData(SpeedRpmChart);
		loadWheelData(wheelChart, false);
		loadDataOnInterval();
	}, 1000);
}
function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
}
function render() {
	controls.update();
	const time =  performance.now() / 1000;
	for ( let i = 0; i < wheels.length; i ++ ) {
		wheels[ i ].rotation.x = time * Math.PI * 2;
	}
	grid.position.z = -( time ) % 1;
	renderer.render( scene, camera );
}
$(() =>{
    init();
});