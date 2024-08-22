import MovieCollections from './MovieCollections'

function App() {
  return (
    <div className="relative bg-gradient-to-l from-slate-600 to-slate-400">
      <div className="sm:py-12 lg:py-12">
        <div className="relative sm:static sm:px-6 lg:px-8">
          <MovieCollections urlCollections="http://localhost:8000/plex/collections/movie/Movies" />
        </div>
      </div>
    </div>
  )
}

export default App
