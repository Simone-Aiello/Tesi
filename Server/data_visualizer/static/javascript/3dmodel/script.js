import * as THREE from 'three';
import Stats from './jsm/libs/stats.module.js';
import { OrbitControls } from './jsm/controls/OrbitControls.js'
import { GLTFLoader } from './jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from './jsm/loaders/DRACOLoader.js';
import { RGBELoader } from './jsm/loaders/RGBELoader.js';
let camera, scene, renderer;
let stats;
let grid;
let controls;
let speed = 0.0;
const wheels = [];
var carModel = undefined;
var raycaster = new THREE.Raycaster();
var mousePointer = new THREE.Vector2();
var initialHeadlightMaterial = undefined;
const emissiveMaterial = new THREE.MeshStandardMaterial({
	color: 0xffffff, 
	emissive: 0xffffff,
});
function onMouseClicked(event){
	mousePointer.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mousePointer.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	raycaster.setFromCamera(mousePointer, camera );
	//Check if cursor intersect headlights, if so changes it's state
	const intersects = raycaster.intersectObjects(scene.children);
	for ( let i = 0; i < intersects.length; i ++ ) {
		if(intersects[i].object.name === "glassCover"){
			carModel.getObjectByName('glassCover').material =  carModel.getObjectByName('glassCover').material == initialHeadlightMaterial ? emissiveMaterial : initialHeadlightMaterial;
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
	controls = new OrbitControls( camera, container );
	controls.enableDamping = true;
	controls.maxDistance = 15;
	controls.target.set( 0, 0.5, 0 );
	controls.update();
	//Create a scene with a grid
	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0x333333 );
	scene.environment = new RGBELoader().load( 'textures/equirectangular/venice_sunset_1k.hdr' );
	scene.environment.mapping = THREE.EquirectangularReflectionMapping;
	const light = new THREE.AmbientLight( 0xffffff );
	scene.add(light);
	grid = new THREE.GridHelper( 100, 100, 0xffffff, 0xffffff );
	grid.material.opacity = 0.2;
	grid.material.depthWrite = false;
	grid.material.transparent = true;
	scene.add( grid );
	// materials
	const bodyMaterial = new THREE.MeshPhysicalMaterial( {
		color: 0xff0000, metalness: 1.0, roughness: 0.5, clearcoat: 1.0, clearcoatRoughness: 0.03, sheen: 0.5
	} );
	const detailsMaterial = new THREE.MeshStandardMaterial( {
		color: 0xffffff, metalness: 1.0, roughness: 0.5
	} );
	const glassMaterial = new THREE.MeshPhysicalMaterial( {
		color: 0xffffff, metalness: 0.25, roughness: 0, transmission: 1.0
	} );

	const bodyColorInput = document.getElementById( 'body-color' );
	bodyColorInput.addEventListener( 'input', function () {
		bodyMaterial.color.set( this.value );
	} );
    const slider = document.getElementById('myRange');
    slider.addEventListener('input',function(){
        //carModel.rotation.y = this.value * -0.8;
        wheels[0].rotation.z = this.value * -0.8;
        wheels[1].rotation.z = this.value * -0.8;
        //grid.rotation.y = this.value * 0.8;
    });
    const verticalSlider = document.getElementById('verticalSlider');
    verticalSlider.addEventListener('input',function(){
		speed = parseFloat(this.value);
    });
	const detailsColorInput = document.getElementById( 'details-color' );
	detailsColorInput.addEventListener( 'input', function () {
		detailsMaterial.color.set( this.value );
	} );
	const glassColorInput = document.getElementById( 'glass-color' );
	glassColorInput.addEventListener( 'input', function () {
		glassMaterial.color.set( this.value );
	} );
	// Car
	//const shadow = new THREE.TextureLoader().load( 'models/gltf/ferrari_ao.png' );
	const dracoLoader = new DRACOLoader();
	dracoLoader.setDecoderPath( 'js/libs/draco/gltf/' );
	const loader = new GLTFLoader();
	loader.setDRACOLoader( dracoLoader );
	loader.load( 'models/gltf/ferrari_458/scene.gltf', function ( gltf ) {
		
		carModel = gltf.scene;
		console.log(carModel);
		console.log(carModel.getObjectByName('chassis'));
		//carModel.getObjectByName('chassis').material.color.set(0xffffff);
		initialHeadlightMaterial = carModel.getObjectByName('glassCover').material;
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
	const loader2 = new GLTFLoader();
	loader2.setDRACOLoader( dracoLoader );
	loader2.load('models/gltf/danger_signs/snow.gltf', function(gltf){
		gltf.scene.position.y = 0.0;
		gltf.scene.position.x = -0.6;
		gltf.scene.position.z = -10;
		gltf.scene.scale.x = 0.5;
		gltf.scene.scale.y = 0.5;
		gltf.scene.scale.z = 0.5;
		gltf.scene.rotation.x = 1.5;
		gltf.scene.rotation.z = 3;
		scene.add(gltf.scene);
	});
}
function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
}
function render() {
	controls.update();
	const time = - performance.now() / 1000;
	for ( let i = 0; i < wheels.length; i ++ ) {
		//if(speed > 0) wheels[ i ].rotation.x = time * Math.PI * 2 + speed;
	}
	//console.log(speed);
	grid.position.z += speed;
	grid.position.z %= 1200;
	//grid.position.x += document.getElementById('myRange').value * -0.3;
	renderer.render( scene, camera );
	stats.update();
}
init();