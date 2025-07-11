
use std::io;

use actix_web::cookie::time::error;
use actix_web::Error;
use mysql::{Pool, PooledConn};
use mysql::prelude::*;
use mysql::params;
use serde::{Serialize};
use serde_json::Value;
use std::io::Write; // <== important !

use std::fs::{self, File};

use std::path::Path;




#[derive(Debug)]
pub struct Boat {
    conn: Option<PooledConn>,
}



#[derive(Debug, Serialize)]
pub struct BoatCollection  {
    pub id: u32,
    pub name: String,
    pub path: String
}

#[derive(Debug, Serialize)]
pub struct BoatCount {
    name: String,
    count: u32
}


impl Boat {
    pub fn new(conn: Option<PooledConn>) -> Self {
        Boat { conn }
    }

    pub fn add_boat(&mut self, name: String, startRecord: String, dataStruct: serde_json::Value) -> Result<bool, Box<dyn std::error::Error>> {

        // add file
        let path_str = format!("./boats/{}", name);
        let path = Path::new(&path_str);

        if !path.exists() {
            // Crée le dossier (avec tous les dossiers parents si besoin)
            fs::create_dir_all(path)?;
            println!("Dossier créé : {}", path.display());
        } else {
            println!("Le dossier existe déjà : {}", path.display());
        }

        let file_path = path.join(format!("{}.json", startRecord ));

        let json_string = serde_json::to_string_pretty(&dataStruct)
            .expect("Erreur lors de la conversion en JSON");

        let mut file = File::create(&file_path)?;
        file.write_all(json_string.as_bytes())?;

        println!("Données enregistrées dans {}", file_path.display());
        

        // add to database:
        let conn = self.conn.as_mut();
        let conn = conn.ok_or("conn is None")?;


        // Annoter le type explicitement ici
        conn.exec_drop(
            "INSERT INTO boats (name, path) VALUES (:name, :path)",
            params! {
                "name" => name,
                "path" => startRecord
            },
        )?;


        
        Ok(true)


    }
    
    // pub fn get_all_boats(&mut self) -> Result<Vec<BoatCollection>, Box<dyn std::error::Error>> {

    //     let conn = self.conn.as_mut(); // 2e Option<&mut>
    //     let conn = conn.ok_or("conn is None")?; // on extrait le &mut PooledConn final

    
    //     let boats: Vec<BoatCollection> = conn
    //         .query_map(
    //             "SELECT id, name, path FROM boats",
    //             |(id, name, path) | BoatCollection {id, name, path}
    //         )?;

    //     Ok(boats)
    // }

    pub fn get_boat_by_id(&mut self, id: i32) -> Result<BoatCollection, Box<dyn std::error::Error>> {

        let conn = self.conn.as_mut();
        let conn = conn.ok_or("conn is None")?;

        let boat = conn
            .exec_first("SELECT id, name, path FROM boats WHERE id=:id;", 
                params! (
                    "id" => id
                ),
            )?
            .ok_or("Boat not found")?;

        let (id, name, path): (u32, String, String) = boat;


        Ok(BoatCollection { id, name, path })
    }

    pub fn get_grouped_boats(&mut self) -> Result<Vec<BoatCount>, Box<dyn std::error::Error>> {

        let conn = self.conn.as_mut();
        let conn = conn.ok_or("conn is None")?;

        let groupBoats: Vec<BoatCount> = conn
            .query_map(
                "SELECT name, COUNT(name) FROM boats GROUP BY name",
                |(name, count) | BoatCount {name, count}
            )?;

        Ok(groupBoats)
    }

    pub fn get_boat_by_name(&mut self, nameBoat: String) -> Result<Vec<BoatCollection>, Box<dyn std::error::Error>> {

        let conn = self.conn.as_mut();
        let conn = conn.ok_or("conn is None")?;

        // let request = format!("SELECT * FROM boats WHERE name = {};", name);

        let groupBoats: Vec<BoatCollection> = conn
            .exec_map(
                "SELECT id, name, path FROM boats WHERE name =:name;",
                params! ("name" => nameBoat),
                |(id, name, path) | BoatCollection {id, name, path}
            )?;

        Ok(groupBoats)

    }
    
}