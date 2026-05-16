use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Seal {
    pub pattern_id: String,
    pub runtime: String,
    pub code_hash: String,
    pub signature: String,
}

pub fn sign(pattern_id: &str, runtime: &str, code_hash: &str, secret: &str) -> Seal {
    let mut h = Sha256::new();
    h.update(pattern_id.as_bytes());
    h.update(runtime.as_bytes());
    h.update(code_hash.as_bytes());
    h.update(secret.as_bytes());
    let sig = hex::encode(h.finalize());
    Seal { pattern_id: pattern_id.into(), runtime: runtime.into(), code_hash: code_hash.into(), signature: sig }
}

pub fn verify(seal: &Seal, secret: &str) -> bool {
    let expected = sign(&seal.pattern_id, &seal.runtime, &seal.code_hash, secret);
    seal.signature == expected.signature
}
