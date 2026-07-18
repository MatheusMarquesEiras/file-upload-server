import { useState } from 'react'
import UploadTab from './components/UploadTab'
import DownloadTab from './components/DownloadTab'
import FilesTab from './components/FilesTab'
import SettingsTab from './components/SettingsTab'
import { useSettings } from './hooks/useSettings'

type Tab = 'upload' | 'download' | 'files' | 'settings'

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: 'upload',   label: 'Enviar',        icon: 'cloud_upload' },
  { id: 'download', label: 'Receber',       icon: 'download' },
  { id: 'files',    label: 'Arquivos',      icon: 'folder_open' },
  { id: 'settings', label: 'Configurações', icon: 'settings' },
]

const TAB_IDS = TABS.map((t) => t.id)

function initialTab(): Tab {
  const hash = window.location.hash.replace('#', '')
  return (TAB_IDS as string[]).includes(hash) ? (hash as Tab) : 'upload'
}

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>(initialTab)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { settings, update } = useSettings()

  const selectTab = (tab: Tab) => {
    setActiveTab(tab)
    setSidebarOpen(false)
    window.history.replaceState(null, '', `#${tab}`)
  }

  return (
    <div className="bg-surface text-on-surface min-h-screen">
      {/* Barra superior móvel */}
      <header className="md:hidden sticky top-0 z-50 h-14 bg-surface-container-lowest border-b border-surface-container-highest flex items-center gap-3 px-4">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 -ml-2 text-secondary active:scale-95 transition-all"
          aria-label="Abrir menu"
        >
          <span className="material-symbols-outlined">menu</span>
        </button>
        <img src="/logo.jpg" alt="WorkAnt" className="w-8 h-8 rounded-lg object-cover" />
        <h1 className="text-lg font-bold tracking-tighter uppercase">WorkAnt</h1>
      </header>

      {/* SideNavBar (rail) — estilo WorkAnt */}
      <aside
        className={`h-screen w-64 fixed left-0 top-0 bg-slate-100 flex flex-col py-6 z-50 transition-transform duration-200 md:translate-x-0 ${
          sidebarOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'
        }`}
      >
        <div className="px-6 mb-10 flex items-center gap-3">
          <img src="/logo.jpg" alt="WorkAnt" className="w-12 h-12 rounded-xl object-cover" />
          <div>
            <h1 className="text-xl font-bold tracking-tighter text-slate-900 uppercase">WorkAnt</h1>
            <p className="text-[10px] uppercase tracking-widest text-secondary font-bold opacity-70">Home Server Uploads</p>
          </div>
        </div>
        <nav className="flex-1 space-y-1">
          {TABS.map((tab) => (
            <NavItem
              key={tab.id}
              icon={tab.icon}
              label={tab.label}
              active={activeTab === tab.id}
              onClick={() => selectTab(tab.id)}
            />
          ))}
        </nav>
        <div className="mt-auto border-t border-slate-200/50 pt-4 px-6">
          <p className="text-[10px] uppercase tracking-widest text-secondary font-bold opacity-70">
            Transferência na rede local
          </p>
        </div>
      </aside>

      {/* Overlay móvel */}
      {sidebarOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/40 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Conteúdo */}
      <main className="md:ml-64 min-h-screen flex flex-col bg-surface">
        <div className="p-4 sm:p-8 lg:p-12 max-w-5xl mx-auto w-full">
          {activeTab === 'upload'   && <UploadTab />}
          {activeTab === 'download' && <DownloadTab settings={settings} />}
          {activeTab === 'files'    && <FilesTab settings={settings} />}
          {activeTab === 'settings' && <SettingsTab settings={settings} update={update} />}
        </div>
      </main>
    </div>
  )
}

function NavItem({ icon, label, active, onClick }: { icon: string; label: string; active?: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 transition-all active:scale-95 duration-150 font-headline tracking-tight text-sm font-semibold ${
        active
          ? 'bg-green-100 text-green-900 border-l-4 border-green-600'
          : 'text-slate-600 hover:bg-slate-200 border-l-4 border-transparent'
      }`}
    >
      <span
        className="material-symbols-outlined"
        style={active ? { fontVariationSettings: "'FILL' 1" } : {}}
      >
        {icon}
      </span>
      <span>{label}</span>
    </button>
  )
}
