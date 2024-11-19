import Navbar from '../../Components/Navbar/Navbar'

import Page from '../../pages/Page'

const Home = () => {
  return (
    <div className='flex'>
      <div>
          <Navbar/>
      </div>
      <div className='w-full'>

        <Page />
      </div>
    </div>
  )
}

export default Home
