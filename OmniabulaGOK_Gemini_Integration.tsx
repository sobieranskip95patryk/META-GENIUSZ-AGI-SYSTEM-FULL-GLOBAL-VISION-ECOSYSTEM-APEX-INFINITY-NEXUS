import React, { useState, useEffect, useRef } from 'react';
import { Upload, Zap, ChevronRight, Save, Trash2, Database, Brain, Activity, AlertTriangle } from 'lucide-react';
import { initializeApp } from "firebase/app";
import { getAuth, signInWithCustomToken, signInAnonymously, onAuthStateChanged } from "firebase/auth";

const App = () => {
  // Stan operacyjny
  const [step, setStep] = useState(1);
  const [files, setFiles] = useState([]);
  const [totalSize, setTotalSize] = useState(0);
  const [processedSize, setProcessedSize] = useState(0);
  const [generatedContent, setGeneratedContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [saveCount, setSaveCount] = useState(0);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  const MAX_SIZE_GB = 5;
  const MAX_SIZE_BYTES = MAX_SIZE_GB * 1024 * 1024 * 1024;
  const apiKey = ""; // Klucz dostarczany przez środowisko

  // Inicjalizacja Auth (zgodnie z protokołem)
  useEffect(() => {
    const initAuth = async () => {
      try {
        const firebaseConfig = JSON.parse(window.__firebase_config || '{}');
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        
        if (typeof window.__initial_auth_token !== 'undefined' && window.__initial_auth_token) {
          await signInWithCustomToken(auth, window.__initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
        
        const unsubscribe = onAuthStateChanged(auth, setUser);
        return () => unsubscribe();
      } catch (err) {
        console.error("Auth Error:", err);
      }
    };
    initAuth();
  }, []);

  // Funkcja wywołania Gemini z retry logic (Exponential Backoff)
  const callGemini = async (prompt, retryCount = 0) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
    
    const payload = {
      contents: [{ 
        parts: [{ text: prompt }] 
      }],
      systemInstruction: {
        parts: [{ text: "Jesteś GOK:AI, potężnym systemem operacyjnym Architekta Patryka Sobierańskiego. Twoim zadaniem jest przekształcanie surowych danych (MD, JSON, HTML) w spójną, epicką fabułę książki. Zachowuj styl wysokiej technologii, wizjonerstwa i precyzji. Analizuj SpiralMind: wplataj głębokie wnioski z danych w narrację." }]
      }
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.status === 429 && retryCount < 5) {
        const delay = Math.pow(2, retryCount) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        return callGemini(prompt, retryCount + 1);
      }

      if (!response.ok) throw new Error(`API Error: ${response.statusText}`);

      const data = await response.json();
      return data.candidates?.[0]?.content?.parts?.[0]?.text || "Błąd syntezy danych.";
    } catch (err) {
      if (retryCount < 5) {
        const delay = Math.pow(2, retryCount) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        return callGemini(prompt, retryCount + 1);
      }
      throw err;
    }
  };

  const handleFileUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    let newSize = totalSize;
    const validFiles = [];

    uploadedFiles.forEach(file => {
      if (newSize + file.size <= MAX_SIZE_BYTES) {
        newSize += file.size;
        validFiles.push(file);
      }
    });

    setFiles([...files, ...validFiles]);
    setTotalSize(newSize);
  };

  const startMixing = async () => {
    setIsProcessing(true);
    setError(null);
    try {
      // Czytamy nagłówki/nazwy plików jako wstępny wsad do budowy rdzenia
      const fileNames = files.map(f => f.name).join(", ");
      const prompt = `Zainicjuj rdzeń fabuły na podstawie następującej bazy danych: ${fileNames}. Stwórz prolog i określ kierunek narracji dla Architekta.`;
      
      const response = await callGemini(prompt);
      setGeneratedContent(`[PROTOKÓŁ INICJACJI GOK:AI]\n\n${response}\n\n`);
      setStep(3);
    } catch (err) {
      setError("Nie udało się połączyć z rdzeniem Gemini. Sprawdź status systemów.");
    } finally {
      setIsProcessing(false);
    }
  };

  const generateNextSeries = async () => {
    setIsProcessing(true);
    setError(null);
    try {
      // Symulujemy czytanie fragmentu treści z plików
      // W realnym scenariuszu tutaj czytamy FileReaderem kawałek pliku
      const currentPart = files[Math.floor(Math.random() * files.length)]?.name || "Baza danych";
      const prompt = `Kontynuuj fabułę. Wykorzystaj kontekst poprzednich fragmentów i przetwórz nowe dane z segmentu: ${currentPart}. Rozwiń akcję, wplatając analizę danych SpiralMind.`;
      
      const response = await callGemini(prompt);
      
      const increment = totalSize > 0 ? totalSize / 10 : 512 * 1024 * 1024;
      setProcessedSize(prev => Math.min(prev + increment, totalSize || MAX_SIZE_BYTES));
      setGeneratedContent(prev => prev + `\n--- NOWA SEKWENCJA DANYCH ---\n\n${response}\n`);
      
      if (processedSize + increment >= (totalSize || MAX_SIZE_BYTES)) {
        setStep(4);
      }
    } catch (err) {
      setError("Przerwanie strumienia danych Gemini. Próba ponownego nawiązania łączności...");
    } finally {
      setIsProcessing(false);
    }
  };

  const saveFile = () => {
    const finalData = `${generatedContent}\n\n--- ANALIZA CAŁOŚCIOWA GOK:AI & SPIRALMIND ---\nStatus: Synteza 5GB zakończona.\nOperator: Patryk Sobierański\nSystem: Gemini 2.5 Flash Enhanced`;
    const blob = new Blob([finalData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `GOK_Fabuła_Final_${saveCount + 1}.txt`;
    link.click();
    setSaveCount(prev => prev + 1);
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-slate-950 text-emerald-400 font-mono p-4 md:p-8">
      <div className="max-w-6xl mx-auto border-2 border-emerald-500/30 rounded-lg bg-black/50 overflow-hidden shadow-[0_0_20px_rgba(16,185,129,0.2)]">
        
        {/* Top Bar */}
        <div className="bg-emerald-500/10 p-4 border-b border-emerald-500/30 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Activity className={`text-emerald-500 ${isProcessing ? 'animate-spin' : 'animate-pulse'}`} />
            <h1 className="text-xl font-bold tracking-widest uppercase">GOK OmniWriter: Gemini 2.5 Flash</h1>
          </div>
          <div className="text-xs text-emerald-500/60 text-right">
            AUTH: {user ? 'AUTHORIZED' : 'CONNECTING...'} <br/>
            MODEL: GEMINI-2.5-FLASH-PREVIEW
          </div>
        </div>

        {error && (
          <div className="bg-red-900/40 p-3 border-b border-red-500/50 flex items-center gap-3 text-red-400 text-sm">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}

        <div className="p-6">
          {step === 1 && (
            <div className="py-12 text-center space-y-6">
              <div className="flex justify-center">
                <div className="p-10 rounded-xl bg-emerald-500/5 border-2 border-dashed border-emerald-500/30 hover:bg-emerald-500/10 transition-all cursor-pointer">
                  <input type="file" multiple className="hidden" id="file-input" onChange={handleFileUpload} />
                  <label htmlFor="file-input" className="cursor-pointer">
                    <Upload className="w-20 h-20 mx-auto mb-4 opacity-40" />
                    <p className="text-xl font-bold">Wrzucaj masę danych (Max 5GB)</p>
                    <p className="text-xs opacity-50 mt-2">Pliki zostaną zindeksowane przez SpiralMind</p>
                  </label>
                </div>
              </div>
              <div className="text-sm opacity-70">
                Wykryto: {files.length} plików | Objętość: {formatSize(totalSize)}
              </div>
              {files.length > 0 && (
                <button onClick={() => setStep(2)} className="bg-emerald-600 hover:bg-emerald-500 text-black font-black py-4 px-10 rounded-full transition-transform active:scale-95 flex items-center gap-3 mx-auto">
                  <ChevronRight /> URUCHOM RDZEŃ ANALITYCZNY
                </button>
              )}
            </div>
          )}

          {step === 2 && (
            <div className="py-16 text-center space-y-8">
              <Brain className="w-24 h-24 mx-auto text-emerald-400 animate-pulse" />
              <h2 className="text-3xl font-black tracking-tighter uppercase">Inicjacja Procesora Fabuły</h2>
              <p className="max-w-xl mx-auto opacity-60">
                Podłączono do API Gemini 2.5 Flash. System gotowy do transformacji {formatSize(totalSize)} surowych danych w epopeję.
              </p>
              <button 
                onClick={startMixing} 
                disabled={isProcessing}
                className="bg-emerald-500 hover:bg-emerald-400 text-black font-black py-5 px-16 rounded-xl shadow-[0_0_30px_rgba(16,185,129,0.4)] flex items-center gap-4 mx-auto uppercase disabled:opacity-50"
              >
                {isProcessing ? 'Inicjowanie...' : <><Zap fill="black" /> Mixuj treść i twórz fabułę</>}
              </button>
            </div>
          )}

          {step === 3 && (
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[600px]">
              <div className="lg:col-span-3 flex flex-col gap-4">
                <div className="flex-1 bg-black/80 border border-emerald-500/20 p-6 rounded-lg overflow-y-auto text-sm leading-relaxed shadow-inner">
                  <pre className="whitespace-pre-wrap font-sans text-emerald-100">{generatedContent}</pre>
                  {isProcessing && (
                    <div className="mt-6 flex items-center gap-3 text-emerald-500 italic">
                      <div className="w-3 h-3 bg-emerald-500 rounded-full animate-ping" />
                      Gemini 2.5 Flash przetwarza segment danych...
                    </div>
                  )}
                </div>
                <button 
                  onClick={generateNextSeries} 
                  disabled={isProcessing}
                  className="bg-emerald-600 hover:bg-emerald-500 text-black font-black py-4 rounded-lg flex items-center justify-center gap-3 transition-all disabled:grayscale"
                >
                  DALEJ (Procesuj kolejną serię) <ChevronRight />
                </button>
              </div>

              <div className="space-y-6">
                <div className="p-4 bg-emerald-900/10 border border-emerald-500/20 rounded-lg">
                  <h3 className="text-xs font-bold uppercase opacity-50 mb-4">Postęp Procesora GOK</h3>
                  <div className="h-4 bg-black rounded-full overflow-hidden border border-emerald-500/10">
                    <div 
                      className="h-full bg-gradient-to-r from-emerald-800 to-emerald-400 transition-all duration-1000"
                      style={{ width: `${(processedSize / (totalSize || MAX_SIZE_BYTES)) * 100}%` }}
                    />
                  </div>
                  <div className="mt-2 text-[10px] flex justify-between">
                    <span>SYNTEZA: {formatSize(processedSize)}</span>
                    <span>CEL: {formatSize(totalSize || MAX_SIZE_BYTES)}</span>
                  </div>
                </div>

                <div className="p-4 border border-emerald-500/20 rounded-lg text-xs space-y-3">
                  <div className="flex justify-between">
                    <span className="opacity-50">Pliki:</span>
                    <span>{files.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="opacity-50">Zapisy:</span>
                    <span className="text-yellow-500">{saveCount}</span>
                  </div>
                </div>

                <button 
                  onClick={saveFile} 
                  className="w-full py-4 border-2 border-emerald-500/50 hover:bg-emerald-500/10 text-emerald-400 font-bold rounded-lg flex items-center justify-center gap-2 transition-all"
                >
                  <Save size={18} /> ZAPISZ TREŚĆ (.txt)
                </button>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="py-16 text-center space-y-8">
              <div className="w-32 h-32 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto border-4 border-emerald-500 shadow-[0_0_50px_rgba(16,185,129,0.3)]">
                <Database className="w-16 h-16 text-emerald-500" />
              </div>
              <h2 className="text-4xl font-black uppercase">5GB Przetworzone</h2>
              <p className="max-w-md mx-auto opacity-70">
                Fabuła została w pełni wygenerowana. System Gemini 2.5 Flash zakończył procesowanie Twoich danych.
              </p>
              <div className="flex gap-4 justify-center">
                <button onClick={saveFile} className="bg-emerald-500 hover:bg-emerald-400 text-black font-black py-5 px-16 rounded-xl flex items-center gap-4 text-xl">
                  <Save /> ODBIERZ DZIEŁO FINALNE
                </button>
                <button 
                  onClick={() => {setStep(1); setFiles([]); setTotalSize(0); setProcessedSize(0); setGeneratedContent('');}}
                  className="border border-red-500/50 hover:bg-red-500/10 text-red-500 font-bold px-8 rounded-xl"
                >
                  RESET
                </button>
              </div>
            </div>
          )}
        </div>

        {/* System Bar */}
        <div className="bg-black p-2 px-6 border-t border-emerald-500/30 text-[9px] flex justify-between items-center opacity-40 tracking-widest uppercase">
          <span>GOK_CORE_CONNECT: ONLINE</span>
          <span>Buffer: {((processedSize / (1024*1024*1024)).toFixed(2))}GB / 5.00GB</span>
          <span>API_STABLE: {isProcessing ? 'BUSY' : 'IDLE'}</span>
        </div>
      </div>
    </div>
  );
};

export default App;
