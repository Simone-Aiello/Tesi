let camera, scene, renderer;
let stats;
let grid;
let controls;
const wheels = [];
var carModel = undefined;
var raycaster = new THREE.Raycaster();
var mousePointer = new THREE.Vector2();
function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}
function loadData(match,clientX,clientY){
	console.log(match)
    $.ajax({
        'url': '/rest_api/VehicleData',
        'type': 'GET',
        'data': {
            vehicle: "FG868XN",
            sensor: [match[1]+"_"+match[2]+"_wheel_pressure"],
			latest: true,
        },
        'success': function (data) {
			console.log(data)
			$(".tooltiptext").css({
				"display": "initial",
				"opacity": "1",
				"top": clientY - $(".tooltiptext").outerHeight(true),
				"left" : clientX - 12,
			});
			$("#sensor_name").text("Sensor: " + capitalizeFirstLetter(match[1]) + " " + match[2] + " tire pressure");
			$("li#value").text("Value: " + data.data);
			$("li#date").text("Date: " + data.timestamp.split("T")[0]);
        },
        'error': function (request, error) {
            console.log("Error reading data");
        }
    });
}
function onMouseClicked(event){
	$(".tooltiptext").css({
		"display" : "none",
		"opacity": "0",
		"top": 0,
		"left" : 0,
	});
	mousePointer.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mousePointer.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	raycaster.setFromCamera(mousePointer, camera );
	const intersects = raycaster.intersectObjects(scene.children);
    //console.log(intersects)
	for ( let i = 0; i < intersects.length; i ++ ) {
		let match = intersects[i].object.name.match(/(front|rear)_(left|right)_(brake|rim|tire)/);
		if(match != null){
			loadData(match,event.clientX,event.clientY);
            break;
		}
        else if(intersects[i].object.name !== ''){
            break;
        }
	}
}
function init() {
	//Raycast to check intersection on click


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
	stats = new Stats();
	container.appendChild( stats.dom );
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
        //console.log(carModel.getObjectByName('chassis'));
		//carModel.getObjectByName('chassis')
        wheels.push(carModel.getObjectByName('rear_left_rim'))
        wheels.push(carModel.getObjectByName('rear_right_rim'))
        wheels.push(carModel.getObjectByName('front_left_rim'))
        wheels.push(carModel.getObjectByName('front_right_rim'))
		const detailsMaterial = new THREE.MeshStandardMaterial( {
			color: 0xFF0000, metalness: 1.0, roughness: 0.5
		});
		carModel.getObjectByName('rear_left_tire').material = carModel.getObjectByName('rear_left_tire').material.clone();
		carModel.getObjectByName('rear_left_tire').material = carModel.getObjectByName('rear_right_tire').material.clone();
		carModel.getObjectByName('rear_left_tire').material = carModel.getObjectByName('front_left_tire').material.clone();
		carModel.getObjectByName('rear_left_tire').material = carModel.getObjectByName('front_right_tire').material.clone();
		//1.6 : 2.6 = x : 0.074  FORMULA DA IMPLEMENTARE PER VEDERE QUANTO UNA RUOTA E' SGONFIA
		carModel.getObjectByName('rear_left_tire').material.color.setRGB(0.045,0,0);
		console.log(carModel.getObjectByName('rear_left_tire')["material"]);
        scene.add(carModel)
		//console.log(xen);
		// carModel = gltf.scene.children[ 0 ];
		// console.log(carModel);
		// carModel.getObjectByName( 'body' ).material = bodyMaterial;
		// carModel.getObjectByName( 'rim_fl' ).material = detailsMaterial;
		// carModel.getObjectByName( 'rim_fr' ).material = detailsMaterial;
		// carModel.getObjectByName( 'rim_rr' ).material = detailsMaterial;
		// carModel.getObjectByName( 'rim_rl' ).material = detailsMaterial;
		// carModel.getObjectByName( 'trim' ).material = detailsMaterial;
		// carModel.getObjectByName( 'glass' ).material = glassMaterial;
		// carModel.getObjectByName( 'glass' ).material = glassMaterial;
		// wheels.push(
		// 	carModel.getObjectByName( 'wheel_fl' ),
		// 	carModel.getObjectByName( 'wheel_fr' ),
		// 	carModel.getObjectByName( 'wheel_rl' ),
		// 	carModel.getObjectByName( 'wheel_rr' )
		// );
		// shadow
		/*const mesh = new THREE.Mesh(
			new THREE.PlaneGeometry( 0.655 * 4, 1.3 * 4 ),
			new THREE.MeshBasicMaterial( {
				map: shadow, blending: THREE.MultiplyBlending, toneMapped: false, transparent: true
			} )
		);
		mesh.rotation.x = - Math.PI / 2;
		mesh.renderOrder = 2;*/
		//carModel.add( mesh );
		//scene.add( spotLight );
		//scene.add( spotLightHelper );
		//display a cone to help with light
		//scene.add( carModel );
	} );
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
	stats.update();
}
$(() =>{
    init();
});