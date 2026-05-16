fn main() {
    let pattern_id = "rs-001";
    let runtime = "rust";
    let code_hash = format!("{:x}", sha2::Sha256::digest(format!("{}{}", pattern_id, runtime).as_bytes()));
    println!("{{"pattern_id":"{}","runtime":"{}","code_hash":"{}"}}", pattern_id, runtime, code_hash);
}
