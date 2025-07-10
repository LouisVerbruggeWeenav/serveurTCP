


use actix_web::{get, post, web, App, HttpServer, Responder, web::Json};
use serde_json;

use pyo3::prelude::*;
use pyo3::types::PyModule;
use std::fs;

use std::ffi::CString;

use std::sync::Mutex;


// Ensure the database module is declared

mod database;
use crate::database::{boat::Boat, connection::Connection};

use serde::Deserialize;

// #[derive(Clone)]
struct AppState {
    boat: Mutex<Boat>,
}


#[derive(Deserialize)]
struct Info {
    id: i32,
}



#[post("/api/boats/one")]
async fn get_boat_one(data: web::Data<AppState>, info: web::Json<Info>) -> impl Responder {
    
    let mut json: serde_json::Value = serde_json::Value::Null;

    let mut boat = data.boat.lock().unwrap(); // <- maintenant tu peux muter !
    match boat.get_boat_by_id(info.id) {
        Ok(boats) => {           

            json = match fs::read_to_string(format!("{}/{}.json", boats.name, boats.path)) {
                Ok(contenu) => { 
                    match serde_json::from_str(&contenu) {
                        Ok(dataJson) => dataJson,
                        
                        Err(e) => {
                            eprintln!("Erreur de parsing JSON : {}", e);
                            serde_json::json!({ "error": format!("Parsing JSON failed: {}", e) })
                        }
                    }
                },
                Err(e) => {
                    let pathFail = format!("{}/{}.json", boats.name, boats.path);
                    eprintln!("Erreur de lecture du fichier : {} {}", e, pathFail);
                    serde_json::json!({ "error": format!("File read failed: {}", e) })
                }
            }
        },
        Err(e) => {
            eprintln!("Erreur lors de la récupération : {}", e);
            json = serde_json::json!({ "error": format!("{}", e) });
            
        }
    }

    Json(json)
}



#[get("/")]
async fn index() -> impl Responder {

    let nom_fichier = "../boats/test/test.json";

    let contenu = fs::read_to_string(nom_fichier).expect("Quelque chose s'est mal passé lors de la lecture du fichier");
    let json: serde_json::Value = serde_json::from_str(&contenu).expect("msg");

    Json(
        json
    )
}



// #[get("/hello/{name}")]
// async fn greet(data: web::Data<AppState>, name: web::Path<String>) -> impl Responder {

//     let mut boat = data.boat.lock().unwrap(); // <- maintenant tu peux muter !
//     let test = boat.getTest();
//     format!("Hello {name} {chiffre}!")
// }




fn function_python() -> PyResult<()> {
    let code_str = fs::read_to_string("./main.py").expect("Fichier Python introuvable");

    let code_cstring = CString::new(code_str).expect("CString::new failed");
    let filename = CString::new("main.py").unwrap();
    let modulename = CString::new("main").unwrap();

    Python::with_gil(|py| {
        let module = PyModule::from_code(py, code_cstring.as_c_str(), filename.as_c_str(), modulename.as_c_str())?;
        module.getattr("run")?.call1(("hello louis".to_string(), ))?;
        Ok(())
    })
}



#[actix_web::main] // or #[tokio::main]
async fn main() -> std::io::Result<()> {
// fn main() {
    let mut database = Connection::new("localhost".to_string(), 3306, "root".to_string(), "welcome1".to_string(), "boat_directory".to_string());
    database.connect();

    // get all data boats:
    let mut boat = Boat::new(database.getConn());


    // GLOBAL_DATA.with(|text| {
    //     println!("Global string is {}", *text.borrow());
    // });



    // GET ALL:
    //
    // match boat.get_all_boats(){
    //     Ok(boats) => {
    //         for boat in boats {
    //             println!("{} | {} | {}", boat.id, boat.name, boat.path);
    //         }
    //     },
    //     Err(e) => {
    //         eprintln!("Erreur lors de la récupération : {}", e);
    //     }
    // }


    // GET ONE:
    //
    // match boat.get_boat_by_id(15) {
    //     Ok(boat) => {
    //         println!("{} | {} | {}", boat.id, boat.name, boat.path);
    //     },
    //     Err(e) => {
    //         eprintln!("Erreur lors de la récupération : {}", e);
    //     }
    // }

    // SCRIPT PYTHON:
    //
    // function_python();


    let config = web::Data::new(AppState { boat: Mutex::new(boat), });



    HttpServer::new(move || {
        App::new()
        .app_data(config.clone())
        .service(
            web::scope("/rust")
                .service(index)
                //.service(greet)
                .service(get_boat_one)
        )
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}





