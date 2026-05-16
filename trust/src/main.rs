use trust::{sign, verify};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let pattern_id = args.get(1).cloned().unwrap_or("demo".into());
    let runtime = args.get(2).cloned().unwrap_or("rust".into());
    let code_hash = args.get(3).cloned().unwrap_or("hash".into());
    let secret = args.get(4).cloned().unwrap_or("secret".into());
    let s = sign(&pattern_id, &runtime, &code_hash, &secret);
    let ok = verify(&s, &secret);
    println!("{}", serde_json::json!({"seal": s, "verified": ok}));
}
