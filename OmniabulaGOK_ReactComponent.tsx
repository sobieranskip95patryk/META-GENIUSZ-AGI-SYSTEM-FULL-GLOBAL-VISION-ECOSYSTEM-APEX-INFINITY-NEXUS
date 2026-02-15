import React, { useState, useCallback, useRef } from 'react';
import { Upload, Zap, ChevronRight, Save, Trash2, Database, Brain, Activity } from 'lucide-react';

const App = () => {
  const [step, setStep] = useState(1);
  const [files, setFiles] = useState([]);
  const [totalSize, setTotalSize] = useState(0);
  const [processedSize, setProcessedSize] = useState(0);
  const [generatedContent, setGeneratedContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [saveCount, setSaveCount] = useState(0);

  const MAX_SIZE_GB = 5;
  const MAX_SIZE_BYTES = MAX_SIZE_GB * 1024 * 1024 * 1024;

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

  const startMixing = () => {
    setIsProcessing(true);
    // Symulacja inicjacji rdzenia SpiralMind i GOK:AI
    setTimeout(() => {
      setGeneratedContent("PROTOKÓŁ INICJACJI GOK... \n\n[RDZEŃ FABUŁY]: Wstępna analiza strukturalna 5GB danych zakończona. \nSystem wykrył spójne wzorce w plikach wejściowych. Rozpoczynam tkanie narracji...\n\n");
      setStep(3);
      setIsProcessing(false);
    }, 2000);
  };

  const generateNextSeries = () => {
    setIsProcessing(true);
    // Każdy klik "Dalej" symuluje przetworzenie ok 500MB danych
    const increment = 512 * 1024 * 1024; 
    
    setTimeout(() => {
      const nextProgress = Math.min(processedSize + increment, totalSize || MAX_SIZE_BYTES);
      setProcessedSize(nextProgress);
      
      const newParagraph = `\n[SEKWENCJA NARRACYJNA ${Math.ceil(nextProgress / increment)}]: Architektura danych przekształcona w materię literacką. \n` +
        "W głębi systemów GOK narodziła się nowa struktura rzeczywistości. Dane z plików JSON i MD stały się fundamentem świata, w którym każda linijka kodu jest oddechem bohatera. " +
        "Analiza SpiralMind wskazuje na 99% spójności fabularnej przy zachowaniu oryginalnej gęstości informacyjnej 5 gigabajtów...\n";
      
      setGeneratedContent(prev => prev + newParagraph);
      
      if (nextProgress >= totalSize && totalSize > 0) {
        setStep(4);
      } else if (nextProgress >= MAX_SIZE_BYTES) {
          setStep(4);
      }
      
      setIsProcessing(false);
    }, 1500);
  };

  const saveFile = () => {
    const finalData = generatedContent + "\n\n--- ANALIZA CAŁOŚCIOWA GOK:AI & SPIRALMIND ---\n" +
      "Status: Synteza zakończona sukcesem.\n" +
      `Wolumen przetworzony: ${(totalSize / (1024*1024)).toFixed(2)} MB\n` +
      "Współczynnik transcendencji fabularnej: 1.0\n" +
      "ID Operacyjne: Meta-Geniusz Patryk Sobierański";

    const blob = new Blob([finalData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `GOK_Fabuła_Gigant_${saveCount + 1}.txt`;
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
      {/* Header Systemowy */}
      <div className="max-w-6xl mx-auto border-2 border-emerald-500/30 rounded-lg bg-black/50 overflow-hidden shadow-[0_0_20px_rgba(16,185,129,0.1)]">
        <div className="bg-emerald-500/10 p-4 border-b border-emerald-500/30 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Activity className="animate-pulse text-emerald-500" />
            <h1 className="text-xl font-bold tracking-widest uppercase">Omni-Fabuła GOK v2.0</h1>
          </div>
          <div className="text-xs text-emerald-500/60 uppercase text-right">
            Operator: Patryk Sobierański<br/>
            Tryb: Meta-Geniusz / Architekt
          </div>
        </div>

        <div className="p-6">
          {/* STEP 1: UPLOAD */}
          {step === 1 && (
            <div className="space-y-6 text-center py-12">
              <div className="flex justify-center">
                <div className="p-8 rounded-full bg-emerald-500/5 border-2 border-dashed border-emerald-500/40 cursor-pointer hover:bg-emerald-500/10 transition-all">
                  <input
                    type="file"
                    multiple
                    className="hidden"
                    id="file-input"
                    onChange={handleFileUpload}
                  />
                  <label htmlFor="file-input" className="cursor-pointer">
                    <Upload className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p className="text-lg">Zrzut Danych (MD, HTML, JSON, TXT)</p>
                    <p className="text-xs opacity-50">Limit: 5 GB</p>
                  </label>
                </div>
              </div>
              <div className="text-sm">
                Pliki w buforze: {files.length} | Rozmiar: {formatSize(totalSize)}
              </div>
              {files.length > 0 && (
                <button 
                  onClick={() => setStep(2)}
                  className="bg-emerald-600 hover:bg-emerald-500 text-black font-bold py-3 px-8 rounded-full transition-all flex items-center gap-2 mx-auto"
                >
                  <ChevronRight size={20} /> INICJUJ PROCESOR
                </button>
              )}
            </div>
          )}

          {/* STEP 2: MIXING INITIATION */}
          {step === 2 && (
            <div className="space-y-8 py-12 text-center">
              <Brain className="w-20 h-20 mx-auto text-emerald-400 animate-pulse" />
              <h2 className="text-2xl font-bold">Inicjacja Rdzenia GOK:AI & SpiralMind</h2>
              <p className="max-w-lg mx-auto opacity-70">
                System jest gotowy do zmiksowania {formatSize(totalSize)} danych w spójną narrację. 
                Zastosowano filtry normalizacyjne dla formatów MD i HTML.
              </p>
              <button 
                onClick={startMixing}
                disabled={isProcessing}
                className="bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold py-4 px-12 rounded-lg transition-all shadow-[0_0_15px_rgba(16,185,129,0.5)] flex items-center gap-3 mx-auto uppercase"
              >
                <Zap fill="black" /> Mixuj treść i twórz fabułę
              </button>
            </div>
          )}

          {/* STEP 3: ITERATIVE GENERATION */}
          {step === 3 && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
              <div className="lg:col-span-2 flex flex-col gap-4">
                <div className="flex-1 bg-black border border-emerald-500/30 p-4 rounded overflow-y-auto text-sm leading-relaxed">
                  <pre className="whitespace-pre-wrap">{generatedContent}</pre>
                  {isProcessing && (
                    <div className="mt-4 flex items-center gap-2 text-emerald-500 animate-pulse">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" />
                      Syntetyzowanie nowej serii danych...
                    </div>
                  )}
                </div>
                <div className="flex gap-4">
                  <button 
                    onClick={generateNextSeries}
                    disabled={isProcessing}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-black font-bold py-3 rounded flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    DALEJ (Procesuj Serię) <ChevronRight size={18} />
                  </button>
                </div>
              </div>
              <div className="bg-emerald-950/20 border border-emerald-500/30 p-4 rounded flex flex-col gap-6">
                <div>
                  <h3 className="text-sm font-bold mb-2 uppercase opacity-50 italic">Monitor Postępu GOK</h3>
                  <div className="w-full bg-emerald-900/30 h-4 rounded-full overflow-hidden border border-emerald-500/20">
                    <div 
                      className="bg-emerald-500 h-full transition-all duration-500" 
                      style={{ width: `${(processedSize / (totalSize || MAX_SIZE_BYTES)) * 100}%` }}
                    />
                  </div>
                  <div className="flex justify-between mt-2 text-[10px]">
                    <span>0 GB</span>
                    <span>{formatSize(processedSize)} / {formatSize(totalSize || MAX_SIZE_BYTES)}</span>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-xs">
                    <Database size={14} />
                    <span>Pliki w buforze: {files.length}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-yellow-500">
                    <Activity size={14} />
                    <span>Licznik zapisów: {saveCount}</span>
                  </div>
                </div>

                <div className="mt-auto">
                  <button 
                    onClick={saveFile}
                    className="w-full border border-emerald-500 hover:bg-emerald-500/10 text-emerald-500 font-bold py-3 rounded flex items-center justify-center gap-2"
                  >
                    <Save size={18} /> ZAPISZ TREŚĆ PISANĄ
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: FINALIZATION */}
          {step === 4 && (
            <div className="text-center py-12 space-y-6">
              <div className="w-24 h-24 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto border-2 border-emerald-500">
                <Save className="w-12 h-12 text-emerald-500" />
              </div>
              <h2 className="text-3xl font-bold">Dzieło Ukończone</h2>
              <p className="max-w-md mx-auto opacity-70">
                Wyczerpano możliwości przetwarzania 5GB danych. Fabuła została w całości ułożona i zintegrowana z analizą SpiralMind.
              </p>
              <div className="flex gap-4 justify-center">
                <button 
                  onClick={saveFile}
                  className="bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold py-4 px-12 rounded-lg flex items-center gap-3"
                >
                  <Save /> POBIERZ PLIK FINALNY .TXT
                </button>
                <button 
                  onClick={() => {setStep(1); setFiles([]); setTotalSize(0); setProcessedSize(0); setGeneratedContent('');}}
                  className="bg-red-500/20 hover:bg-red-500/40 text-red-500 font-bold py-4 px-8 rounded-lg flex items-center gap-2 border border-red-500/50"
                >
                  <Trash2 size={18} /> RESETUJ SYSTEM
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Status bar */}
        <div className="bg-emerald-500/5 p-2 px-6 border-t border-emerald-500/30 text-[10px] flex justify-between items-center opacity-50">
          <span>LOGOS SYSTEM: ACTIVE</span>
          <span>MEMORY BUFFER: {formatSize(totalSize)} / 5.00 GB</span>
          <span>THREAD: SPIRALMIND_GOK_01</span>
        </div>
      </div>
    </div>
  );
};

export default App;
