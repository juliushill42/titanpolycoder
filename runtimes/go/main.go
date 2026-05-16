package main
import (
  "crypto/sha256"
  "encoding/hex"
  "encoding/json"
  "fmt"
  "os"
  "path/filepath"
)
type Payload struct {PatternID string `json:"pattern_id"`; Runtime string `json:"runtime"`; CodeHash string `json:"code_hash"`}
func main(){
  patternID := "go-001"
  runtime := "go"
  h:=sha256.Sum256([]byte(patternID+runtime))
  payload:=Payload{PatternID:patternID, Runtime:runtime, CodeHash:hex.EncodeToString(h[:])}
  b,_:=json.MarshalIndent(payload,"","  ")
  _=os.MkdirAll(filepath.Join("..","..","data"), 0755)
  _=os.WriteFile(filepath.Join("..","..","data","go-001.json"),b,0644)
  fmt.Println(string(b))
}
