fn main() {
    println!("cargo:rustc-link-lib=python3.8");
    println!("cargo:rerun-if-changed=build.rs");
}
